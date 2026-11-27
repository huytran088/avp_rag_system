"""Eval-only generation server. Never deploy it.

Same prompt path as /api/generate (avp_rag.generate), but:
- no cache, so repeated samples of one request are independent;
- no rate limit;
- no provider fallback, so every sample comes from the configured model;
- per-call switches for the ablations (RAG on/off, k, reranker);
- each response records the provider, model, temperature, prompt hash and latency.

Run: uv run uvicorn evals.server:app --port 8799
"""

import hashlib
import os
import threading
import time
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from avp_rag import config
from avp_rag import providers
from avp_rag import retrieve as retrieval
from avp_rag.generate import build_prompt

load_dotenv(config.ENV_FILE)

_MODEL_ENV = {
    "anthropic": ("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
    "vllm": ("VLLM_MODEL", "qwen3.6-27b-awq"),
    "hf": ("HF_MODEL", providers.DEFAULT_HF_MODEL),
    "gemini": ("GEMINI_MODEL", providers.DEFAULT_GEMINI_MODEL),
}
_TEMPERATURE_ENV = {"vllm": "VLLM_TEMPERATURE"}

# Flipping use_reranker must not interleave with another request's retrieval
_rerank_lock = threading.Lock()


def call_llm(prompt: str) -> str:
    """The configured provider only: an outage must show up as a failed sample."""
    return providers._get_provider_fn(providers.get_provider_name())(prompt)


def _model_info() -> dict:
    name = providers.get_provider_name()
    env, default = _MODEL_ENV.get(name, ("", ""))
    temp_env = _TEMPERATURE_ENV.get(name, "LLM_TEMPERATURE")
    return {
        "provider": name,
        "model": os.environ.get(env, default) if env else "",
        "temperature": float(os.environ.get(temp_env, "0.6")),
    }


@asynccontextmanager
async def lifespan(_app: FastAPI):
    retrieval.get_retriever()
    yield


app = FastAPI(title="AVP eval server", lifespan=lifespan)


class GenerateBody(BaseModel):
    query: str = Field(min_length=1)
    code: str | None = None
    instructions: str | None = None
    rag: bool = True
    k: int = Field(default=2, ge=1, le=10)


class RetrieveBody(BaseModel):
    query: str = Field(min_length=1)
    k: int = Field(default=5, ge=1, le=20)
    rerank: bool = True


def _retrieve(query: str, k: int, rerank: bool = True):
    retriever = retrieval.get_retriever()
    with _rerank_lock:
        retriever.use_reranker = rerank
        try:
            return retriever.retrieve(query, k=k)
        finally:
            retriever.use_reranker = True


@app.post("/generate")
def generate(body: GenerateBody):
    snippets = []
    if body.rag:
        search = f"{body.query}\n\n{body.code}" if body.code else body.query
        snippets = _retrieve(search, body.k)
    prompt = build_prompt(body.query, snippets, body.code, body.instructions)

    start = time.perf_counter()
    try:
        text = call_llm(prompt)
    except Exception as e:  # Reported per sample, not retried
        raise HTTPException(status_code=502, detail=f"{type(e).__name__}: {e}") from e
    latency_ms = (time.perf_counter() - start) * 1000

    return {
        "generated_code": text,
        "retrieved_functions": [s["function_name"] for s in snippets],
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "latency_ms": latency_ms,
        **_model_info(),
    }


@app.post("/retrieve")
def retrieve(body: RetrieveBody):
    results = _retrieve(body.query, body.k, body.rerank)
    return {"results": [{"function_name": r["function_name"], "score": r["score"]} for r in results]}
