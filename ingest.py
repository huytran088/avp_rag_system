"""CLI shim: `uv run python ingest.py` (same as `python -m avp_rag.ingest`)."""

from avp_rag.ingest import main

if __name__ == "__main__":
    main()
