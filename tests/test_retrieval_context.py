"""Functions are indexed with their file title and the comment above them, so
a request like "QuickSort" can find Lomuto_Partition."""

import json
from unittest.mock import MagicMock, patch

import numpy as np

from avp_rag import retrieve
from avp_rag.ingest import parse_file, run_ingest
from avp_rag.knowledge_base import load_kb

PARTITION_SRC = """// Lomuto Partition

a1 = arr[3, 1, 2]

// Partitions an array around its last element,
// the step QuickSort repeats on each half
fun Lomuto_Partition(@init<table> array, low, high):
    return low
end fun

// A helper with no description above it

fun Helper(x):
    return x
end fun

result = Lomuto_Partition(a1, 0, 2)
"""


def test_parse_file_records_title_and_description(tmp_path):
    path = tmp_path / "lomuto.avp"
    path.write_text(PARTITION_SRC)
    part, helper = parse_file(path)

    assert part["title"] == "Lomuto Partition"
    assert part["description"] == (
        "Partitions an array around its last element,\n"
        "the step QuickSort repeats on each half"
    )
    # A blank line separates a comment from the function, so it isn't its description
    assert helper["title"] == "Lomuto Partition"
    assert helper["description"] == ""


def test_title_is_not_a_function_description(tmp_path):
    path = tmp_path / "f.avp"
    path.write_text("// Only a title\nfun F(x):\n    return x\nend fun\n")
    (f,) = parse_file(path)
    assert f["title"] == "Only a title"
    assert f["description"] == ""


KB = [
    {
        "name": "Lomuto_Partition",
        "parameters": ["array", "low", "high"],
        "code_content": "fun Lomuto_Partition(array, low, high):\nend fun",
        "title": "Lomuto Partition",
        "description": "The step QuickSort repeats",
    },
    {"name": "legacy", "parameters": [], "code_content": "fun legacy():\nend fun"},
]


def _retriever(tmp_path, embedder, reranker=None):
    path = tmp_path / "kb.json"
    path.write_text(json.dumps({"metadata": {}, "chunks": KB}))
    with (
        patch.object(retrieve, "FlagModel", return_value=embedder),
        patch.object(retrieve, "FlagReranker", return_value=reranker or MagicMock()),
    ):
        return retrieve.CodeRetriever(
            knowledge_base_path=path, use_reranker=reranker is not None
        )


def _embedder():
    embedder = MagicMock()
    embedder.encode.return_value = np.eye(2, dtype="float32")
    embedder.encode_queries.return_value = np.array([[1.0, 0.0]], dtype="float32")
    return embedder


def test_index_text_includes_title_and_description(tmp_path):
    embedder = _embedder()
    r = _retriever(tmp_path, embedder)

    (texts,), _ = embedder.encode.call_args
    assert texts[0] == (
        "Lomuto Partition: The step QuickSort repeats\n"
        "Function: Lomuto_Partition(array, low, high)\n"
        "fun Lomuto_Partition(array, low, high):\nend fun"
    )
    # Entries from an older knowledge base (no title/description) still work
    assert texts[1] == "Function: legacy()\nfun legacy():\nend fun"
    assert r.code_texts == texts


def test_reranker_sees_the_same_text_as_the_index(tmp_path):
    reranker = MagicMock()
    reranker.compute_score.return_value = [1.0, 0.5]
    r = _retriever(tmp_path, _embedder(), reranker)

    r.retrieve("QuickSort", k=1)

    (pairs,), _ = reranker.compute_score.call_args
    assert ("QuickSort", r.code_texts[0]) in pairs


def test_run_ingest_rebuilds_an_old_format_kb(tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    (data / "lomuto.avp").write_text(PARTITION_SRC)
    kb = tmp_path / "kb.json"

    run_ingest(data_dir=data, kb_path=kb)
    # Simulate a knowledge base written before titles/descriptions existed
    chunks, metadata = load_kb(kb)
    for c in chunks:
        c.pop("title")
        c.pop("description")
    metadata.pop("kb_format", None)
    kb.write_text(json.dumps({"metadata": metadata, "chunks": chunks}))

    result = run_ingest(data_dir=data, kb_path=kb)

    assert result.changed  # unchanged file re-parsed because the format is old
    chunks, metadata = load_kb(kb)
    assert all("description" in c for c in chunks)
    assert metadata["kb_format"] == 2
    assert run_ingest(data_dir=data, kb_path=kb).changed == []
