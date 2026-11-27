"""Tests for the optional `code` / `instructions` fields of /api/generate.

Retrieval must use only the user's request (plus the editor code), never the
client's language rules, and the cache key must cover every field.
"""

from unittest.mock import patch

from tests.conftest import MOCK_LLM_OUTPUT, MOCK_RETRIEVE_RESULT

CODE = "a1 = arr[3, 1, 2]"
RULES = "All function names must start with a capital letter."


def _patched():
    return (
        patch("avp_rag.generate.retrieve_code", return_value=MOCK_RETRIEVE_RESULT),
        patch("avp_rag.generate.call_llm", return_value=MOCK_LLM_OUTPUT),
    )


class TestBuildPrompt:
    def test_plain_query_prompt_has_no_extra_sections(self):
        from avp_rag.generate import build_prompt

        prompt = build_prompt("add numbers", MOCK_RETRIEVE_RESULT)
        assert "TASK: add numbers" in prompt
        assert "CURRENT CODE" not in prompt
        assert "Additional rules" not in prompt

    def test_code_and_instructions_get_their_own_sections(self):
        from avp_rag.generate import build_prompt

        prompt = build_prompt(
            "sort it", MOCK_RETRIEVE_RESULT, code=CODE, instructions=RULES
        )
        assert "TASK: sort it" in prompt
        assert f"--- CURRENT CODE START ---\n{CODE}\n--- CURRENT CODE END ---" in prompt
        assert f"Additional rules:\n{RULES}" in prompt
        # The rules must not leak into the TASK line
        assert "TASK: sort it\n" in prompt


class TestBuildContext:
    def test_retrieval_uses_query_only(self):
        from avp_rag import generate

        retrieve_p, llm_p = _patched()
        with retrieve_p as retrieve, llm_p:
            generate.build_context("sort it", instructions=RULES)
        retrieve.assert_called_once_with("sort it", k=2)

    def test_retrieval_uses_query_and_code_not_instructions(self):
        from avp_rag import generate

        retrieve_p, llm_p = _patched()
        with retrieve_p as retrieve, llm_p:
            generate.build_context("sort it", code=CODE, instructions=RULES)
        (text,), _ = retrieve.call_args
        assert text == f"sort it\n\n{CODE}"
        assert RULES not in text


class TestGenerateEndpoint:
    def test_accepts_code_and_instructions(self, client):
        retrieve_p, llm_p = _patched()
        with retrieve_p as retrieve, llm_p as llm:
            resp = client.post(
                "/api/generate",
                json={"query": "sort it", "code": CODE, "instructions": RULES},
            )
        assert resp.status_code == 200
        assert resp.json()["generated_code"] == MOCK_LLM_OUTPUT
        (text,), _ = retrieve.call_args
        assert RULES not in text
        (prompt,), _ = llm.call_args
        assert CODE in prompt and RULES in prompt

    def test_query_only_still_works(self, client):
        resp = client.post("/api/generate", json={"query": "add numbers"})
        assert resp.status_code == 200

    def test_cache_key_includes_code(self, client):
        retrieve_p, llm_p = _patched()
        with retrieve_p, llm_p as llm:
            first = client.post("/api/generate", json={"query": "fix it", "code": "x = 1"})
            second = client.post("/api/generate", json={"query": "fix it", "code": "x = 2"})
            repeat = client.post("/api/generate", json={"query": "fix it", "code": "x = 2"})
        assert first.json()["cached"] is False
        assert second.json()["cached"] is False
        assert repeat.json()["cached"] is True
        assert llm.call_count == 2

    def test_cache_key_includes_instructions(self, client):
        retrieve_p, llm_p = _patched()
        with retrieve_p, llm_p as llm:
            client.post("/api/generate", json={"query": "q", "instructions": "a"})
            resp = client.post("/api/generate", json={"query": "q", "instructions": "b"})
        assert resp.json()["cached"] is False
        assert llm.call_count == 2

    def test_empty_query_rejected(self, client):
        resp = client.post("/api/generate", json={"query": ""})
        assert resp.status_code == 422

    def test_overlong_fields_rejected(self, client):
        assert client.post("/api/generate", json={"query": "q" * 2001}).status_code == 422
        assert (
            client.post("/api/generate", json={"query": "q", "code": "x" * 20001}).status_code
            == 422
        )
        assert (
            client.post(
                "/api/generate", json={"query": "q", "instructions": "x" * 8001}
            ).status_code
            == 422
        )
