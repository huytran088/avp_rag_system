import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Ensure project root is on sys.path so retrieve/generate imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

load_dotenv(PROJECT_ROOT / ".env")

from .routes import router
from .dependencies import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Eagerly initialize the retriever at startup
    import asyncio
    from retrieve import get_retriever
    await asyncio.to_thread(get_retriever)
    yield


app = FastAPI(title="AVP RAG API", lifespan=lifespan)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — extend with CORS_ORIGINS env var (comma-separated) for deployed frontends
_default_origins = ["http://localhost:5173", "http://localhost:3000"]
_extra_origins = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", "").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_default_origins + _extra_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router)

# Serve built frontend from static/ if it exists
static_dir = PROJECT_ROOT / "static"
if static_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
