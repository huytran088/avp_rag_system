import asyncio
import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from avp_rag import config
from avp_rag import retrieve as retrieval

from .dependencies import limiter
from .routes import router

# Must run before CORS_ORIGINS is read below; providers read env at call time
load_dotenv(config.ENV_FILE)

# uvicorn only configures its own loggers; without this, INFO messages from
# the app (e.g. the rate-limit key note in api.dependencies) are dropped
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s - %(message)s")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Eagerly initialize the retriever at startup (slow: model loading)
    await asyncio.to_thread(retrieval.get_retriever)
    yield


app = FastAPI(title="AVP RAG API", lifespan=lifespan)

# Rate limiting
app.state.limiter = limiter
# slowapi's handler signature is narrower than Starlette's ExceptionHandler type
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # pyright: ignore[reportArgumentType]

# CORS — extend with CORS_ORIGINS env var (comma-separated) for deployed frontends
_DEFAULT_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]
_extra_origins = [o.strip() for o in os.environ.get("CORS_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_DEFAULT_ORIGINS + _extra_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Serve built frontend from static/ if it exists
if config.STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(config.STATIC_DIR), html=True), name="static")
