import asyncio
import hashlib
import json

from fastapi import APIRouter, HTTPException, Request

from avp_rag import generate as generation
from avp_rag import retrieve as retrieval
from avp_rag.providers import get_provider_name, is_provider_configured

from .cache import generation_cache, retrieval_cache
from .dependencies import limiter
from .models import (
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
    RetrievedFunction,
    RetrieveRequest,
    RetrieveResponse,
)

router = APIRouter(prefix="/api")


@router.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        retriever_loaded=retrieval.is_retriever_loaded(),
        provider_configured=is_provider_configured(),
    )


@router.post("/retrieve", response_model=RetrieveResponse)
@limiter.limit("30/minute")
async def retrieve(body: RetrieveRequest, request: Request):
    cache_key = f"{body.query}:{body.k}"
    cached = retrieval_cache.get(cache_key)
    if cached is not None:
        return RetrieveResponse(results=cached, cached=True)

    raw = await asyncio.to_thread(retrieval.retrieve_code, body.query, body.k)
    results = [RetrievedFunction(**r) for r in raw]
    retrieval_cache.set(cache_key, results)
    return RetrieveResponse(results=results, cached=False)


def _generate_cache_key(body: GenerateRequest) -> str:
    """Plain query keeps its old key; requests with code/instructions hash every field."""
    if body.code is None and body.instructions is None:
        return body.query
    payload = json.dumps([body.query, body.code, body.instructions])
    return hashlib.sha256(payload.encode()).hexdigest()


@router.post("/generate", response_model=GenerateResponse)
@limiter.limit("10/minute")
async def generate(body: GenerateRequest, request: Request):
    if not is_provider_configured():
        raise HTTPException(
            status_code=503, detail=f"{get_provider_name()} provider is not configured"
        )

    cache_key = _generate_cache_key(body)
    cached = generation_cache.get(cache_key)
    if cached is not None:
        return GenerateResponse(**cached, cached=True)

    result = await asyncio.to_thread(
        generation.generate_code,
        body.query,
        code=body.code,
        instructions=body.instructions,
    )

    response_data = {
        "generated_code": result["generated_code"],
        "retrieved_functions": [
            RetrievedFunction(**r) for r in result["retrieved_functions"]
        ],
    }
    generation_cache.set(cache_key, response_data)
    return GenerateResponse(**response_data, cached=False)
