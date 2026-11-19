"""Tests for avp_rag.ingest (ANTLR parsing + incremental knowledge base build)."""

from avp_rag.ingest import parse_file, run_ingest
from avp_rag.knowledge_base import load_kb
from avp_rag.tracking import source_key

ADD_SRC = """fun add(a, b):
    return a + b
end fun

result = add(1, 2)
"""

MUL_SRC = """fun mul(a, b):
    return a * b
end fun
"""


def test_parse_file_extracts_function(tmp_path):
    path = tmp_path / "add.avp"
    path.write_text(ADD_SRC)
    funcs = parse_file(path, source_file="add.avp")
    assert len(funcs) == 1
    f = funcs[0]
    assert f["name"] == "add"
    assert f["parameters"] == ["a", "b"]
    assert f["code_content"].startswith("fun add(a, b):")
    assert f["code_content"].endswith("end fun")
    assert f["source_file"] == "add.avp"


def test_run_ingest_incremental(tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    kb = tmp_path / "kb.json"
    (data / "add.avp").write_text(ADD_SRC)
    (data / "mul.avp").write_text(MUL_SRC)

    first = run_ingest(data, kb)
    assert first.previous_ingestion is None
    assert len(first.changed) == 2
    assert sorted(c["name"] for c in first.chunks) == ["add", "mul"]

    chunks, metadata = load_kb(kb)
    assert sorted(c["name"] for c in chunks) == ["add", "mul"]
    assert set(metadata["source_files"]) == {source_key(data / "add.avp"), source_key(data / "mul.avp")}

    # Nothing changed: everything preserved, nothing re-parsed
    second = run_ingest(data, kb)
    assert second.changed == []
    assert second.preserved_count == 2
    assert second.previous_ingestion is not None

    # Delete one file: its chunks disappear
    (data / "mul.avp").unlink()
    third = run_ingest(data, kb)
    assert third.deleted == [source_key(data / "mul.avp")]
    assert [c["name"] for c in third.chunks] == ["add"]


def test_run_ingest_records_parse_failures(tmp_path, monkeypatch):
    data = tmp_path / "data"
    data.mkdir()
    (data / "add.avp").write_text(ADD_SRC)

    def boom(*_args, **_kwargs):
        raise RuntimeError("parse failed")

    monkeypatch.setattr("avp_rag.ingest.parse_file", boom)
    result = run_ingest(data, tmp_path / "kb.json")
    assert result.failed == [(source_key(data / "add.avp"), "parse failed")]
    assert result.chunks == []
