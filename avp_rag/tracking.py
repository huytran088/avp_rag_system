"""
File modification tracking for AVP ingest system.

Hash-based change detection to enable incremental ingestion of .avp source files.
Files are keyed by their path relative to PROJECT_ROOT (e.g. "data/foo.avp"),
or by absolute path when they live outside the project.
"""

import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from . import config
from .knowledge_base import PathLike, empty_metadata, load_kb

__all__ = [
    "compute_file_hash",
    "detect_changed_files",
    "empty_metadata",
    "load_metadata",
    "remove_deleted_from_metadata",
    "resolve_source_key",
    "source_key",
    "update_metadata",
]


def source_key(path: PathLike) -> str:
    """Stable metadata key for a source file."""
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(config.PROJECT_ROOT).as_posix()
    except ValueError:
        return str(resolved)


def resolve_source_key(key: str) -> Path:
    """Inverse of source_key: absolute path on disk."""
    return config.PROJECT_ROOT / key


def compute_file_hash(file_path: PathLike) -> str:
    """Compute SHA256 hex digest of file contents."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in 64KB chunks for memory efficiency
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_metadata(kb_path: PathLike) -> Dict:
    """Metadata from the knowledge base, or empty metadata if missing/legacy."""
    _, metadata = load_kb(kb_path)
    return metadata


def detect_changed_files(
    data_folder: PathLike,
    metadata: Dict,
    file_extension: str = config.SOURCE_EXTENSION,
) -> Tuple[List[str], List[str], List[str]]:
    """
    Detect which files changed since the last ingestion using hash comparison.

    Returns (changed, unchanged, deleted) as lists of source keys (see source_key).
    """
    source_files = metadata.get("source_files", {})
    changed_files: List[str] = []
    unchanged_files: List[str] = []
    current_files = set()

    for filename in sorted(os.listdir(data_folder)):
        if not filename.endswith(file_extension):
            continue
        key = source_key(Path(data_folder) / filename)
        current_files.add(key)

        current_hash = compute_file_hash(resolve_source_key(key))
        previous_hash = source_files.get(key, {}).get("hash")

        if current_hash == previous_hash:
            unchanged_files.append(key)
        else:
            # New file (no previous hash) or modified file
            changed_files.append(key)

    # Deleted: in metadata but no longer on disk
    deleted_files = [f for f in source_files if f not in current_files]

    return changed_files, unchanged_files, deleted_files


def remove_deleted_from_metadata(metadata: Dict, deleted_files: List[str]) -> Dict:
    """Remove deleted files from metadata (mutates and returns it)."""
    source_files = metadata.get("source_files", {})
    for key in deleted_files:
        source_files.pop(key, None)
    return metadata


def update_metadata(metadata: Dict, key: str, function_names: List[str]) -> Dict:
    """Record a file's hash/size/functions after ingestion (mutates and returns metadata)."""
    path = resolve_source_key(key)
    metadata.setdefault("source_files", {})[key] = {
        "hash": compute_file_hash(path),
        "mtime": os.path.getmtime(path),
        "size": os.path.getsize(path),
        "functions": function_names,
    }
    metadata["last_ingestion"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return metadata
