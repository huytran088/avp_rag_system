"""CLI shim: `uv run python retrieve.py` (same as `python -m avp_rag.retrieve`)."""

from avp_rag.retrieve import main

if __name__ == "__main__":
    main()
