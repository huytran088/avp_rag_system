"""Integration tests for LLM provider fallback through the API."""

import os
from unittest.mock import MagicMock, patch

from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.testclient import TestClient

from tests.conftest import MOCK_LLM_OUTPUT, MOCK_RETRIEVE_RESULT


def _setup(env_overrides: dict | None = None):
    """Common setup: mock retriever, fresh limiter, env patch context.

    Returns (app, mock_retriever, env, fresh_limiter) for callers to
    compose their own ``with`` blocks.
    """
    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = MOCK_RETRIEVE_RESULT

    env = {
        "ANTHROPIC_API_KEY": "fake-key-for-testing",
        "LLM_PROVIDER": "anthropic",
    }
    if env_overrides:
        env.update(env_overrides)

    from api.main import app
    from api.cache import generation_cache, retrieval_cache

    generation_cache.clear()
    retrieval_cache.clear()

    fresh_limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = fresh_limiter

    return app, mock_retriever, env, fresh_limiter


class TestProviderFallback:
    def test_generate_uses_primary_provider(self):
        app, mock_retriever, env, fresh_limiter = _setup()
        mock_anthropic = MagicMock(return_value=MOCK_LLM_OUTPUT)

        with (
            patch("retrieve._retriever", mock_retriever),
            patch.dict(os.environ, env, clear=True),
            patch("api.dependencies.limiter", fresh_limiter),
            patch("api.routes.limiter", fresh_limiter),
            patch("providers._call_anthropic", mock_anthropic),
            TestClient(app) as client,
        ):
            resp = client.post("/api/generate", json={"message": "add numbers"})
            assert resp.status_code == 200
            assert resp.json()["generated_code"] == MOCK_LLM_OUTPUT
            mock_anthropic.assert_called()

    def test_generate_falls_back_to_vllm(self):
        app, mock_retriever, env, fresh_limiter = _setup(
            env_overrides={"LLM_FALLBACK_PROVIDER": "vllm"},
        )
        fallback_code = "fun fallback():\n    return 0\nend fun"
        mock_anthropic = MagicMock(side_effect=RuntimeError("API key invalid"))
        mock_vllm = MagicMock(return_value=fallback_code)

        with (
            patch("retrieve._retriever", mock_retriever),
            patch.dict(os.environ, env, clear=True),
            patch("api.dependencies.limiter", fresh_limiter),
            patch("api.routes.limiter", fresh_limiter),
            patch("providers._call_anthropic", mock_anthropic),
            patch("providers._call_vllm", mock_vllm),
            TestClient(app) as client,
        ):
            resp = client.post("/api/generate", json={"message": "add numbers"})
            assert resp.status_code == 200
            assert resp.json()["generated_code"] == fallback_code
            mock_vllm.assert_called()

    def test_generate_503_when_not_configured(self):
        """No API key -> is_provider_configured() returns False -> 503."""
        app, mock_retriever, _, fresh_limiter = _setup()
        env_no_key = {"LLM_PROVIDER": "anthropic"}  # No ANTHROPIC_API_KEY

        with (
            patch("retrieve._retriever", mock_retriever),
            patch.dict(os.environ, env_no_key, clear=True),
            patch("api.dependencies.limiter", fresh_limiter),
            patch("api.routes.limiter", fresh_limiter),
            TestClient(app) as client,
        ):
            resp = client.post("/api/generate", json={"message": "add numbers"})
            assert resp.status_code == 503
            assert "not configured" in resp.json()["detail"]

    def test_health_reflects_provider_status(self):
        app, mock_retriever, _, fresh_limiter = _setup()

        # With API key -> configured
        with (
            patch("retrieve._retriever", mock_retriever),
            patch.dict(os.environ, {
                "LLM_PROVIDER": "anthropic",
                "ANTHROPIC_API_KEY": "fake",
            }, clear=True),
            patch("api.dependencies.limiter", fresh_limiter),
            patch("api.routes.limiter", fresh_limiter),
            TestClient(app) as client,
        ):
            resp = client.get("/api/health")
            assert resp.json()["provider_configured"] is True

        # Without API key -> not configured
        with (
            patch("retrieve._retriever", mock_retriever),
            patch.dict(os.environ, {
                "LLM_PROVIDER": "anthropic",
            }, clear=True),
            patch("api.dependencies.limiter", fresh_limiter),
            patch("api.routes.limiter", fresh_limiter),
            TestClient(app) as client,
        ):
            resp = client.get("/api/health")
            assert resp.json()["provider_configured"] is False

    def test_generate_500_when_all_providers_fail(self):
        app, mock_retriever, env, fresh_limiter = _setup(
            env_overrides={"LLM_FALLBACK_PROVIDER": "vllm"},
        )
        mock_anthropic = MagicMock(side_effect=RuntimeError("primary down"))
        mock_vllm = MagicMock(side_effect=RuntimeError("fallback down"))

        with (
            patch("retrieve._retriever", mock_retriever),
            patch.dict(os.environ, env, clear=True),
            patch("api.dependencies.limiter", fresh_limiter),
            patch("api.routes.limiter", fresh_limiter),
            patch("providers._call_anthropic", mock_anthropic),
            patch("providers._call_vllm", mock_vllm),
            TestClient(app, raise_server_exceptions=False) as client,
        ):
            resp = client.post("/api/generate", json={"message": "add numbers"})
            assert resp.status_code == 500
