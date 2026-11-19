"""Tests for avp_rag.knowledge_base (shared KB reader/writer)."""

import json

import pytest

from avp_rag.knowledge_base import empty_metadata, load_kb, save_kb

CHUNK = {"type": "function", "name": "f", "parameters": [], "code_content": "fun f():\nend fun"}


def test_missing_file_returns_empty(tmp_path):
    chunks, metadata = load_kb(tmp_path / "nope.json")
    assert chunks == []
    assert metadata == empty_metadata()


def test_missing_file_raises_when_not_ok(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_kb(tmp_path / "nope.json", missing_ok=False)


def test_legacy_list_format(tmp_path):
    path = tmp_path / "kb.json"
    path.write_text(json.dumps([CHUNK]))
    chunks, metadata = load_kb(path)
    assert chunks == [CHUNK]
    assert metadata == empty_metadata()


def test_tracked_format_round_trip(tmp_path):
    path = tmp_path / "kb.json"
    meta = {"last_ingestion": "2026-01-01T00:00:00Z", "tracking_method": "hash", "source_files": {}}
    save_kb([CHUNK], meta, path)
    assert load_kb(path) == ([CHUNK], meta)


def test_unknown_format_raises(tmp_path):
    path = tmp_path / "kb.json"
    path.write_text(json.dumps({"something": "else"}))
    with pytest.raises(ValueError):
        load_kb(path)
