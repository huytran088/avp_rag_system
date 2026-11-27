"""Which client address the rate limiter keys on.

On HF Spaces every request arrives from HF's proxy, so keying on the socket
peer would put all users in one bucket. The client address must come from a
proxy header, and only from one the deployment's proxy actually sets:
otherwise a client can send that header itself and dodge the limit.
"""

import logging
import os
from unittest.mock import patch

import pytest
from starlette.requests import Request

from api import dependencies
from api.dependencies import client_ip


def _request(headers=None, peer="10.0.0.1"):
    scope = {
        "type": "http",
        "headers": [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()],
        "client": (peer, 1234),
    }
    return Request(scope)


@pytest.fixture(autouse=True)
def _clean_env():
    keys = ("RATE_LIMIT_IP_SOURCE", "FORWARDED_TRUSTED_HOPS")
    env = {k: v for k, v in os.environ.items() if k not in keys}
    with patch.dict(os.environ, env, clear=True):
        dependencies._logged_forwarded_shape = False
        yield


def _env(**values):
    return patch.dict(os.environ, {k: str(v) for k, v in values.items()})


class TestDefaultXRealIp:
    """The capstone nginx overwrites X-Real-IP, so it is trusted by default."""

    def test_uses_x_real_ip(self):
        assert client_ip(_request({"X-Real-IP": " 1.2.3.4 "})) == "1.2.3.4"

    def test_ignores_x_forwarded_for(self):
        assert client_ip(_request({"X-Forwarded-For": "9.9.9.9"})) == "10.0.0.1"

    def test_falls_back_to_peer(self):
        assert client_ip(_request()) == "10.0.0.1"


class TestXForwardedFor:
    """HF Spaces: the proxy appends the address it saw to X-Forwarded-For."""

    def test_uses_rightmost_entry_by_default(self):
        with _env(RATE_LIMIT_IP_SOURCE="x-forwarded-for"):
            assert client_ip(_request({"X-Forwarded-For": "5.6.7.8"})) == "5.6.7.8"

    def test_ignores_entries_a_client_prepended(self):
        with _env(RATE_LIMIT_IP_SOURCE="x-forwarded-for"):
            req = _request({"X-Forwarded-For": "6.6.6.6, 5.6.7.8"})
            assert client_ip(req) == "5.6.7.8"

    def test_counts_trusted_hops_from_the_right(self):
        with _env(RATE_LIMIT_IP_SOURCE="x-forwarded-for", FORWARDED_TRUSTED_HOPS=2):
            req = _request({"X-Forwarded-For": "6.6.6.6, 5.6.7.8, 10.1.1.1"})
            assert client_ip(req) == "5.6.7.8"

    def test_short_header_uses_its_first_entry(self):
        with _env(RATE_LIMIT_IP_SOURCE="x-forwarded-for", FORWARDED_TRUSTED_HOPS=3):
            assert client_ip(_request({"X-Forwarded-For": "5.6.7.8"})) == "5.6.7.8"

    def test_ignores_a_client_supplied_x_real_ip(self):
        with _env(RATE_LIMIT_IP_SOURCE="x-forwarded-for"):
            req = _request({"X-Real-IP": "6.6.6.6", "X-Forwarded-For": "5.6.7.8"})
            assert client_ip(req) == "5.6.7.8"

    def test_falls_back_to_peer_without_the_header(self):
        with _env(RATE_LIMIT_IP_SOURCE="x-forwarded-for"):
            assert client_ip(_request()) == "10.0.0.1"

    def test_logs_the_header_shape_once_without_addresses(self, caplog):
        with _env(RATE_LIMIT_IP_SOURCE="x-forwarded-for"), caplog.at_level(logging.INFO):
            client_ip(_request({"X-Forwarded-For": "6.6.6.6, 5.6.7.8"}))
            client_ip(_request({"X-Forwarded-For": "7.7.7.7"}))
        messages = [r.getMessage() for r in caplog.records if r.name == "api.dependencies"]
        assert len(messages) == 1
        assert "2 entries" in messages[0]
        assert "6.6.6.6" not in messages[0] and "5.6.7.8" not in messages[0]


def test_peer_source_ignores_all_headers():
    with _env(RATE_LIMIT_IP_SOURCE="peer"):
        req = _request({"X-Real-IP": "1.2.3.4", "X-Forwarded-For": "5.6.7.8"})
        assert client_ip(req) == "10.0.0.1"


def test_unknown_source_is_rejected():
    with _env(RATE_LIMIT_IP_SOURCE="cookie"), pytest.raises(ValueError):
        client_ip(_request())


class TestPerUserBuckets:
    """Through the API: users behind the same proxy get separate limits."""

    def test_two_users_behind_one_proxy_have_separate_limits(self, client):
        with _env(RATE_LIMIT_IP_SOURCE="x-forwarded-for"):
            for i in range(10):
                resp = client.post(
                    "/api/generate",
                    json={"query": f"a {i}"},
                    headers={"X-Forwarded-For": "1.1.1.1"},
                )
                assert resp.status_code == 200
            over = client.post(
                "/api/generate", json={"query": "a over"}, headers={"X-Forwarded-For": "1.1.1.1"}
            )
            other = client.post(
                "/api/generate", json={"query": "b 0"}, headers={"X-Forwarded-For": "2.2.2.2"}
            )
        assert over.status_code == 429
        assert other.status_code == 200

    def test_spoofed_prefix_does_not_reset_the_limit(self, client):
        with _env(RATE_LIMIT_IP_SOURCE="x-forwarded-for"):
            codes = [
                client.post(
                    "/api/generate",
                    json={"query": f"s {i}"},
                    headers={"X-Forwarded-For": f"9.9.9.{i}, 1.1.1.1"},
                ).status_code
                for i in range(11)
            ]
        assert codes[:10] == [200] * 10
        assert codes[10] == 429
