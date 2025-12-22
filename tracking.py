"""
File modification tracking for AVP ingest system.

This module provides hash-based file change detection to enable incremental
ingestion of .avp source files.
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional


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


def load_metadata(kb_path: str) -> Dict:
    """
    Load metadata from knowledge base file.

    Args:
        kb_path: Path to knowledge base JSON file

    Returns:
        Metadata dict with 'source_files' and 'last_ingestion' keys.
        Returns empty metadata structure if file doesn't exist or is old format.
    """
    if not os.path.exists(kb_path):
        return {
            "last_ingestion": None,
            "tracking_method": "hash",
            "source_files": {}
        }

    with open(kb_path, 'r') as f:
        data = json.load(f)

    # Check format
    if isinstance(data, list):
        # Old format - no metadata available
        return {
            "last_ingestion": None,
            "tracking_method": "hash",
            "source_files": {}
        }
    elif isinstance(data, dict) and "metadata" in data:
        # New format with metadata
        return data["metadata"]
    else:
        # Unknown format
        return {
            "last_ingestion": None,
            "tracking_method": "hash",
            "source_files": {}
        }


def load_existing_chunks(kb_path: str) -> List[Dict]:
    """
    Load existing chunks from knowledge base file.

    Args:
        kb_path: Path to knowledge base JSON file

    Returns:
        List of chunk dicts
    """
    if not os.path.exists(kb_path):
        return []

    with open(kb_path, 'r') as f:
        data = json.load(f)

    # Check format
    if isinstance(data, list):
        # Old format - direct array
        return data
    elif isinstance(data, dict) and "chunks" in data:
        # New format with metadata wrapper
        return data["chunks"]
    else:
        return []


def save_with_metadata(chunks: List[Dict], metadata: Dict, kb_path: str):
    """
    Save chunks and metadata to knowledge base file in new format.

    Args:
        chunks: List of code chunk dicts
        metadata: Metadata dict with tracking information
        kb_path: Path to knowledge base JSON file
    """
    output = {
        "metadata": metadata,
        "chunks": chunks
    }

    with open(kb_path, 'w') as f:
        json.dump(output, f, indent=4)


def detect_changed_files(
    data_folder: str,
    metadata: Dict,
    file_extension: str = ".avp"
) -> Tuple[List[str], List[str]]:
    """
    Detect which files have changed since last ingestion using hash comparison.

    Args:
        data_folder: Directory containing source files
        metadata: Metadata dict with previous file hashes
        file_extension: File extension to search for (default: ".avp")

    Returns:
        Tuple of (changed_files, unchanged_files) as lists of full paths
    """
    changed_files = []
    unchanged_files = []

    source_files = metadata.get("source_files", {})

    for filename in os.listdir(data_folder):
        if filename.endswith(file_extension):
            full_path = os.path.join(data_folder, filename)

            # Compute current hash
            current_hash = compute_file_hash(full_path)
            current_mtime = os.path.getmtime(full_path)
            current_size = os.path.getsize(full_path)

            # Check if file has previous metadata
            if full_path in source_files:
                previous_hash = source_files[full_path].get("hash")

                if current_hash == previous_hash:
                    # Hash matches - file unchanged
                    unchanged_files.append(full_path)
                else:
                    # Hash differs - file changed
                    changed_files.append(full_path)
            else:
                # New file - no previous hash
                changed_files.append(full_path)

    return changed_files, unchanged_files


def update_metadata(
    metadata: Dict,
    file_path: str,
    function_names: List[str]
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
    file_hash = compute_file_hash(file_path)
    file_mtime = os.path.getmtime(file_path)
    file_size = os.path.getsize(file_path)

    metadata["source_files"][file_path] = {
        "hash": file_hash,
        "mtime": file_mtime,
        "size": file_size,
        "functions": function_names
    }

    metadata["last_ingestion"] = datetime.utcnow().isoformat() + "Z"

    return metadata
