import asyncio

from fastapi import APIRouter, HTTPException, Request

from providers import get_provider_name, is_provider_configured

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
    from retrieve import _retriever
    return HealthResponse(
        status="ok",
        retriever_loaded=_retriever is not None,
        provider_configured=is_provider_configured(),
    )


@router.post("/retrieve", response_model=RetrieveResponse)
@limiter.limit("30/minute")
async def retrieve(body: RetrieveRequest, request: Request):
    cache_key = f"{body.query}:{body.k}"
    cached = retrieval_cache.get(cache_key)
    if cached is not None:
        return RetrieveResponse(results=cached, cached=True)

    from retrieve import retrieve_code
    raw = await asyncio.to_thread(retrieve_code, body.query, body.k)
    results = [RetrievedFunction(**r) for r in raw]
    retrieval_cache.set(cache_key, results)
    return RetrieveResponse(results=results, cached=False)


@router.post("/generate", response_model=GenerateResponse)
@limiter.limit("10/minute")
async def generate(body: GenerateRequest, request: Request):
    if not is_provider_configured():
        raise HTTPException(status_code=503, detail=f"{get_provider_name()} provider is not configured")

    cached = generation_cache.get(body.message)
    if cached is not None:
        return GenerateResponse(**cached, cached=True)

    from generate import generate_code
    result = await asyncio.to_thread(generate_code, body.message)

    response_data = {
        "generated_code": result["generated_code"],
        "retrieved_functions": [RetrievedFunction(**r) for r in result["retrieved_functions"]],
    }
    generation_cache.set(body.message, response_data)
    return GenerateResponse(**response_data, cached=False)
