"""Eval-only server (evals/server.py): uncached, unlimited, per-call switches."""

import hashlib
import os
from unittest.mock import MagicMock, patch

import pytest
from starlette.testclient import TestClient

from tests.conftest import MOCK_RETRIEVE_RESULT


@pytest.fixture()
def eval_client():
    mock_retriever = MagicMock()
    mock_retriever.use_reranker = True
    mock_retriever.retrieve.return_value = MOCK_RETRIEVE_RESULT
    llm = MagicMock(return_value="```\nresult = 1\n```")
    env = {"LLM_PROVIDER": "hf", "HF_TOKEN": "fake", "LLM_TEMPERATURE": "0.6"}
    with (
        patch("avp_rag.retrieve._retriever", mock_retriever),
        patch("evals.server.call_llm", llm),
        patch.dict(os.environ, env),
    ):
        from evals.server import app

        with TestClient(app) as c:
            yield c, llm, mock_retriever


def test_generate_is_not_cached(eval_client):
    c, llm, _ = eval_client
    for _ in range(3):
        r = c.post("/generate", json={"query": "bubble sort"})
        assert r.status_code == 200
    assert llm.call_count == 3


def test_generate_returns_metadata(eval_client):
    c, llm, _ = eval_client
    body = c.post("/generate", json={"query": "bubble sort"}).json()
    prompt = llm.call_args.args[0]
    assert body["generated_code"] == "```\nresult = 1\n```"
    assert body["provider"] == "hf"
    assert body["model"]
    assert body["temperature"] == 0.6
    assert body["prompt_sha256"] == hashlib.sha256(prompt.encode()).hexdigest()
    assert body["latency_ms"] >= 0
    assert body["retrieved_functions"] == ["addNumbers"]


def test_generate_without_rag_has_no_references(eval_client):
    c, llm, retriever = eval_client
    body = c.post("/generate", json={"query": "bubble sort", "rag": False}).json()
    prompt = llm.call_args.args[0]
    retriever.retrieve.assert_not_called()
    assert "fun addNumbers" not in prompt
    assert body["retrieved_functions"] == []


def test_generate_passes_code_and_instructions(eval_client):
    c, llm, _ = eval_client
    c.post("/generate", json={"query": "q", "code": "x = 1", "instructions": "RULE"})
    prompt = llm.call_args.args[0]
    assert "x = 1" in prompt and "RULE" in prompt


def test_generate_never_falls_back():
    """A provider error is reported, not hidden behind the fallback model."""
    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = MOCK_RETRIEVE_RESULT
    gemini = MagicMock(return_value="from gemini")
    env = {"LLM_PROVIDER": "hf", "HF_TOKEN": "fake", "LLM_FALLBACK_PROVIDER": "gemini"}
    with (
        patch("avp_rag.retrieve._retriever", mock_retriever),
        patch("avp_rag.providers._call_hf", side_effect=RuntimeError("down")),
        patch("avp_rag.providers._call_gemini", gemini),
        patch.dict(os.environ, env),
    ):
        from evals.server import app

        with TestClient(app) as c:
            r = c.post("/generate", json={"query": "q"})
    assert r.status_code == 502
    assert "down" in r.json()["detail"]
    gemini.assert_not_called()


def test_retrieve_can_disable_reranker(eval_client):
    c, _, retriever = eval_client
    seen = []
    retriever.retrieve.side_effect = lambda q, k: seen.append(retriever.use_reranker) or MOCK_RETRIEVE_RESULT
    c.post("/retrieve", json={"query": "q", "k": 5, "rerank": False})
    c.post("/retrieve", json={"query": "q", "k": 5})
    assert seen == [False, True]
    assert retriever.use_reranker is True
