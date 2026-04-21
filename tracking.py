"""
File modification tracking for AVP ingest system.

This module provides hash-based file change detection to enable incremental
ingestion of .avp source files.
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple


def _empty_metadata() -> Dict:
    return {
        "last_ingestion": None,
        "tracking_method": "hash",
        "source_files": {},
    }


def compute_file_hash(file_path: str) -> str:
    """
    Compute SHA256 hash of file contents.

    Args:
        file_path: Path to the file to hash

    Returns:
        Hex string of SHA256 hash
    """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Read in 64KB chunks for memory efficiency
        for chunk in iter(lambda: f.read(65536), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def _read_kb(kb_path: str):
    """Return parsed JSON contents of the knowledge base, or None if missing."""
    if not os.path.exists(kb_path):
        return None
    with open(kb_path, 'r') as f:
        return json.load(f)


def load_metadata(kb_path: str) -> Dict:
    """
    Load metadata from knowledge base file.

    Args:
        kb_path: Path to knowledge base JSON file

    Returns:
        Metadata dict with 'source_files' and 'last_ingestion' keys.
        Returns empty metadata structure if file doesn't exist or is old format.
    """
    data = _read_kb(kb_path)
    if isinstance(data, dict) and "metadata" in data:
        return data["metadata"]
    # Missing file, legacy list format, or unknown format
    return _empty_metadata()


def load_existing_chunks(kb_path: str) -> List[Dict]:
    """
    Load existing chunks from knowledge base file.

    Args:
        kb_path: Path to knowledge base JSON file

    Returns:
        List of chunk dicts
    """
    data = _read_kb(kb_path)
    if isinstance(data, list):
        # Old format - direct array
        return data
    if isinstance(data, dict) and "chunks" in data:
        # New format with metadata wrapper
        return data["chunks"]
    return []


def save_with_metadata(chunks: List[Dict], metadata: Dict, kb_path: str):
    """
    Save chunks and metadata to knowledge base file in new format.

    Args:
        chunks: List of code chunk dicts
        metadata: Metadata dict with tracking information
        kb_path: Path to knowledge base JSON file
    """
    with open(kb_path, 'w') as f:
        json.dump({"metadata": metadata, "chunks": chunks}, f, indent=4)


def detect_changed_files(
    data_folder: str,
    metadata: Dict,
    file_extension: str = ".avp",
) -> Tuple[List[str], List[str], List[str]]:
    """
    Detect which files have changed since last ingestion using hash comparison.

    Args:
        data_folder: Directory containing source files
        metadata: Metadata dict with previous file hashes
        file_extension: File extension to search for (default: ".avp")

    Returns:
        Tuple of (changed_files, unchanged_files, deleted_files) as lists of full paths
    """
    source_files = metadata.get("source_files", {})
    changed_files: List[str] = []
    unchanged_files: List[str] = []
    current_files = set()

    for filename in os.listdir(data_folder):
        if not filename.endswith(file_extension):
            continue
        full_path = os.path.join(data_folder, filename)
        current_files.add(full_path)

        current_hash = compute_file_hash(full_path)
        previous_hash = source_files.get(full_path, {}).get("hash")

        if current_hash == previous_hash:
            unchanged_files.append(full_path)
        else:
            # New file (no previous hash) or modified file
            changed_files.append(full_path)

    # Detect deleted files: in metadata but no longer on disk
    deleted_files = [f for f in source_files if f not in current_files]

    return changed_files, unchanged_files, deleted_files


def remove_deleted_from_metadata(metadata: Dict, deleted_files: List[str]) -> Dict:
    """
    Remove deleted files from metadata.

    Args:
        metadata: Metadata dict to update
        deleted_files: List of file paths that have been deleted

    Returns:
        Updated metadata dict
    """
    source_files = metadata.get("source_files", {})
    for file_path in deleted_files:
        source_files.pop(file_path, None)
    return metadata


def update_metadata(
    metadata: Dict,
    file_path: str,
    function_names: List[str],
) -> Dict:
    """
    Update metadata for a specific file after ingestion.

    Args:
        metadata: Metadata dict to update
        file_path: Path to the file that was ingested
        function_names: List of function names extracted from this file

    Returns:
        Updated metadata dict
    """
    metadata["source_files"][file_path] = {
        "hash": compute_file_hash(file_path),
        "mtime": os.path.getmtime(file_path),
        "size": os.path.getsize(file_path),
        "functions": function_names,
    }
    metadata["last_ingestion"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return metadata
