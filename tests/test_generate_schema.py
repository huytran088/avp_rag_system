"""Regression tests for the /api/generate request schema (issue #3)."""


class TestGenerateRequestSchema:
    def test_query_field_accepted(self, client):
        resp = client.post("/api/generate", json={"query": "add numbers"})
        assert resp.status_code == 200
        assert resp.json()["generated_code"] is not None

    def test_legacy_message_field_rejected(self, client):
        """The old `message` field was renamed to `query`; sending it must 422."""
        resp = client.post("/api/generate", json={"message": "add numbers"})
        assert resp.status_code == 422
        locs = [err["loc"] for err in resp.json()["detail"]]
        assert ["body", "query"] in locs
