"""Reading and writing the knowledge base JSON.

Two on-disk formats are supported:
- legacy: a flat list of chunks
- tracked: {"metadata": {...}, "chunks": [...]}
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

PathLike = str | Path


def empty_metadata() -> Dict:
    return {
        "last_ingestion": None,
        "tracking_method": "hash",
        "source_files": {},
    }


def load_kb(path: PathLike, *, missing_ok: bool = True) -> Tuple[List[Dict], Dict]:
    """Return (chunks, metadata).

    A missing file gives ([], empty metadata) unless missing_ok is False.
    The legacy list format gives empty metadata. An unknown format raises ValueError.
    """
    path = Path(path)
    if not path.exists():
        if missing_ok:
            return [], empty_metadata()
        raise FileNotFoundError(path)

    with open(path, "r") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data, empty_metadata()
    if isinstance(data, dict) and "chunks" in data:
        return data["chunks"], data.get("metadata") or empty_metadata()
    raise ValueError(f"Unknown knowledge base format in {path}")


def save_kb(chunks: List[Dict], metadata: Dict, path: PathLike) -> None:
    """Write chunks and metadata in the tracked format."""
    with open(path, "w") as f:
        json.dump({"metadata": metadata, "chunks": chunks}, f, indent=4)
