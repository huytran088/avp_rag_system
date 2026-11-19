"""Tests for avp_rag.generate."""

import os
from unittest.mock import patch

from tests.conftest import MOCK_LLM_OUTPUT, MOCK_RETRIEVE_RESULT


def test_generate_code_returns_empty_when_nothing_retrieved():
    from avp_rag import generate

    with (
        patch("avp_rag.generate.retrieve_code", return_value=[]),
        patch("avp_rag.generate.call_llm") as llm,
    ):
        result = generate.generate_code("anything")
    assert result == {"generated_code": None, "retrieved_functions": [], "prompt": None}
    llm.assert_not_called()


def test_generate_code_builds_prompt_and_calls_llm():
    from avp_rag import generate

    with (
        patch("avp_rag.generate.retrieve_code", return_value=MOCK_RETRIEVE_RESULT),
        patch("avp_rag.generate.call_llm", return_value=MOCK_LLM_OUTPUT) as llm,
    ):
        result = generate.generate_code("add numbers")
    assert result["generated_code"] == MOCK_LLM_OUTPUT
    assert result["retrieved_functions"] == MOCK_RETRIEVE_RESULT
    assert "TASK: add numbers" in result["prompt"]
    assert MOCK_RETRIEVE_RESULT[0]["code"] in result["prompt"]
    llm.assert_called_once_with(result["prompt"])


def test_generate_solution_retrieves_once():
    """Regression: generate_solution used to retrieve, then call generate_code which retrieved again."""
    from avp_rag import generate

    with (
        patch("avp_rag.generate.retrieve_code", return_value=MOCK_RETRIEVE_RESULT) as retrieve,
        patch("avp_rag.generate.call_llm", return_value=MOCK_LLM_OUTPUT),
        patch.dict(os.environ, {"LLM_PROVIDER": "anthropic", "ANTHROPIC_API_KEY": "k"}),
    ):
        out = generate.generate_solution("add numbers")
    assert out == MOCK_LLM_OUTPUT
    assert retrieve.call_count == 1


def test_generate_solution_simulation_mode_skips_llm():
    from avp_rag import generate

    with (
        patch("avp_rag.generate.retrieve_code", return_value=MOCK_RETRIEVE_RESULT),
        patch("avp_rag.generate.call_llm") as llm,
        patch.dict(os.environ, {"LLM_PROVIDER": "anthropic"}, clear=True),
    ):
        assert generate.generate_solution("add numbers") is None
    llm.assert_not_called()
