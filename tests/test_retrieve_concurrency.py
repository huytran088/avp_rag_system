"""CodeRetriever.retrieve is serialized: HF fast tokenizers are not thread-safe,
and concurrent API requests failed with "RuntimeError: Already borrowed"."""

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock, patch

import numpy as np

from avp_rag import retrieve

KB = [
    {"name": "alpha", "parameters": [], "code_content": "fun alpha():\nend fun"},
    {"name": "beta", "parameters": [], "code_content": "fun beta():\nend fun"},
]


def _retriever(tmp_path, embedder):
    path = tmp_path / "kb.json"
    path.write_text(json.dumps({"metadata": {}, "chunks": KB}))
    with (
        patch.object(retrieve, "FlagModel", return_value=embedder),
        patch.object(retrieve, "FlagReranker", return_value=MagicMock()),
    ):
        return retrieve.CodeRetriever(knowledge_base_path=path, use_reranker=False)


def _embedder():
    embedder = MagicMock()
    embedder.encode.return_value = np.eye(2, dtype="float32")
    return embedder


def test_retrieve_is_serialized_across_threads(tmp_path):
    embedder = _embedder()
    active = 0
    overlaps = []
    guard = threading.Lock()

    def encode_queries(_queries):  # noqa: ARG001
        nonlocal active
        with guard:
            active += 1
            overlaps.append(active)
        time.sleep(0.02)
        with guard:
            active -= 1
        return np.array([[1.0, 0.0]], dtype="float32")

    embedder.encode_queries.side_effect = encode_queries
    r = _retriever(tmp_path, embedder)

    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda q: r.retrieve(q, k=1), ["a", "b", "c", "d"]))

    assert max(overlaps) == 1
