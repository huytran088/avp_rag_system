"""Tests for avp_rag.retrieve with embedding/reranker models mocked out."""

import json
import os
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from avp_rag import retrieve

KB = [
    {"name": "alpha", "parameters": ["x"], "code_content": "fun alpha(x):\nend fun"},
    {"name": "beta", "parameters": [], "code_content": "fun beta():\nend fun"},
    {"name": "gamma", "parameters": [], "code_content": "fun gamma():\nend fun"},
]


@pytest.fixture()
def kb_path(tmp_path):
    path = tmp_path / "kb.json"
    path.write_text(json.dumps({"metadata": {}, "chunks": KB}))
    return path


@pytest.fixture()
def models():
    """Embedding: one-hot per document; query vector closest to alpha, then beta, then gamma."""
    embedder = MagicMock()
    embedder.encode.return_value = np.eye(3, dtype="float32")
    embedder.encode_queries.return_value = np.array([[0.9, 0.5, 0.1]], dtype="float32")
    reranker = MagicMock()
    with (
        patch.object(retrieve, "FlagModel", return_value=embedder) as flag_model,
        patch.object(retrieve, "FlagReranker", return_value=reranker) as flag_reranker,
    ):
        yield flag_model, flag_reranker, reranker


def test_device_none_reads_env(kb_path, models):
    """Regression: device defaulted to "cpu", so EMBEDDING_DEVICE was never read."""
    flag_model, _, _ = models
    with patch.dict(os.environ, {"EMBEDDING_DEVICE": "cuda:1"}):
        r = retrieve.CodeRetriever(knowledge_base_path=kb_path, use_reranker=False)
    assert r.device == "cuda:1"
    assert flag_model.call_args.kwargs["devices"] == "cuda:1"


def test_device_defaults_to_cpu(kb_path, models):
    with patch.dict(os.environ, {}, clear=True):
        r = retrieve.CodeRetriever(knowledge_base_path=kb_path, use_reranker=False)
    assert r.device == "cpu"


def test_vector_search_order_without_reranker(kb_path, models):
    r = retrieve.CodeRetriever(knowledge_base_path=kb_path, use_reranker=False, device="cpu")
    results = r.retrieve("q", k=2)
    assert [x["function_name"] for x in results] == ["alpha", "beta"]
    assert set(results[0]) == {"score", "function_name", "parameters", "code"}


def test_reranker_reorders(kb_path, models):
    _, _, reranker = models
    # Candidates arrive as alpha, beta, gamma; reranker prefers gamma
    reranker.compute_score.return_value = [0.1, 0.2, 0.9]
    r = retrieve.CodeRetriever(knowledge_base_path=kb_path, use_reranker=True, device="cpu")
    results = r.retrieve("q", k=1)
    assert results[0]["function_name"] == "gamma"
    assert results[0]["score"] == pytest.approx(0.9)


def test_is_retriever_loaded():
    with patch.object(retrieve, "_retriever", None):
        assert retrieve.is_retriever_loaded() is False
    with patch.object(retrieve, "_retriever", MagicMock()):
        assert retrieve.is_retriever_loaded() is True
