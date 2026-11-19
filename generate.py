"""CLI shim: `uv run python generate.py` (same as `python -m avp_rag.generate`)."""

from avp_rag.generate import main

if __name__ == "__main__":
    main()
