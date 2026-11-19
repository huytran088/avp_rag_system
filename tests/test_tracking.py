"""Tests for avp_rag.tracking (hash-based change detection)."""

from avp_rag import config
from avp_rag.knowledge_base import empty_metadata
from avp_rag.tracking import (
    detect_changed_files,
    remove_deleted_from_metadata,
    resolve_source_key,
    source_key,
    update_metadata,
)


def test_source_key_relative_inside_project():
    key = source_key(config.DATA_DIR / "foo.avp")
    assert key == "data/foo.avp"
    assert resolve_source_key(key) == config.DATA_DIR / "foo.avp"


def test_source_key_absolute_outside_project(tmp_path):
    key = source_key(tmp_path / "foo.avp")
    assert key == str((tmp_path / "foo.avp").resolve())
    assert resolve_source_key(key) == (tmp_path / "foo.avp").resolve()


def test_detect_changed_unchanged_deleted(tmp_path):
    (tmp_path / "a.avp").write_text("x = 1\n")
    (tmp_path / "b.avp").write_text("y = 2\n")
    (tmp_path / "ignored.txt").write_text("nope")

    metadata = empty_metadata()
    changed, unchanged, deleted = detect_changed_files(tmp_path, metadata)
    assert len(changed) == 2 and unchanged == [] and deleted == []

    for key in changed:
        update_metadata(metadata, key, [])
    assert metadata["last_ingestion"] is not None

    # Modify a, delete b, add c
    (tmp_path / "a.avp").write_text("x = 100\n")
    (tmp_path / "b.avp").unlink()
    (tmp_path / "c.avp").write_text("z = 3\n")

    changed, unchanged, deleted = detect_changed_files(tmp_path, metadata)
    assert sorted(changed) == sorted([source_key(tmp_path / "a.avp"), source_key(tmp_path / "c.avp")])
    assert unchanged == []
    assert deleted == [source_key(tmp_path / "b.avp")]

    remove_deleted_from_metadata(metadata, deleted)
    assert source_key(tmp_path / "b.avp") not in metadata["source_files"]


def test_unchanged_file_detected(tmp_path):
    (tmp_path / "a.avp").write_text("x = 1\n")
    metadata = empty_metadata()
    (key,), _, _ = detect_changed_files(tmp_path, metadata)
    update_metadata(metadata, key, ["f"])
    assert metadata["source_files"][key]["functions"] == ["f"]

    changed, unchanged, deleted = detect_changed_files(tmp_path, metadata)
    assert changed == [] and unchanged == [key] and deleted == []
