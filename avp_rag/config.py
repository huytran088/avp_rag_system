"""Central paths and defaults. All paths are absolute, so nothing depends on the cwd."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
KB_PATH = PROJECT_ROOT / "code_knowledge_base.json"
STATIC_DIR = PROJECT_ROOT / "static"
ENV_FILE = PROJECT_ROOT / ".env"

SOURCE_EXTENSION = ".avp"

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
RERANKER_MODEL = "BAAI/bge-reranker-base"
