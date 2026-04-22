"""Integration tests for slowapi rate limiting through the API."""


class TestRateLimiting:
    def test_generate_rate_limit_enforced(self, client):
        """10 requests succeed, 11th gets 429."""
        for i in range(10):
            resp = client.post("/api/generate", json={"message": f"request {i}"})
            assert resp.status_code == 200, f"Request {i} failed: {resp.status_code}"

        resp = client.post("/api/generate", json={"message": "one too many"})
        assert resp.status_code == 429

    def test_retrieve_rate_limit_enforced(self, client):
        """30 requests succeed, 31st gets 429."""
        for i in range(30):
            resp = client.post("/api/retrieve", json={"query": f"query {i}"})
            assert resp.status_code == 200, f"Request {i} failed: {resp.status_code}"

        resp = client.post("/api/retrieve", json={"query": "one too many"})
        assert resp.status_code == 429

    def test_health_not_rate_limited(self, client):
        """Health endpoint has no rate limit."""
        for _ in range(50):
            resp = client.get("/api/health")
            assert resp.status_code == 200

    def test_rate_limit_response_body(self, client):
        """429 response contains rate-limit text."""
        for i in range(10):
            client.post("/api/generate", json={"message": f"request {i}"})

        resp = client.post("/api/generate", json={"message": "over limit"})
        assert resp.status_code == 429
        assert "Rate limit exceeded" in resp.text
