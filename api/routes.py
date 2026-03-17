import os
import asyncio
from fastapi import APIRouter, Request, HTTPException

from .models import (
    GenerateRequest, GenerateResponse, RetrievedFunction,
    HealthResponse, RetrieveRequest, RetrieveResponse,
)
from .cache import retrieval_cache, generation_cache
from .dependencies import limiter

router = APIRouter(prefix="/api")

@router.get("/health", response_model=HealthResponse)
async def health(request: Request):
    from retrieve import _retriever
    return HealthResponse(
        status="ok",
        retriever_loaded=_retriever is not None,
        api_key_configured=bool(os.environ.get("ANTHROPIC_API_KEY")),
    )

@router.post("/retrieve", response_model=RetrieveResponse)
@limiter.limit("30/minute")
async def retrieve(body: RetrieveRequest, request: Request):
    cached = retrieval_cache.get(f"{body.query}:{body.k}")
    if cached is not None:
        return RetrieveResponse(results=cached, cached=True)

    from retrieve import retrieve_code
    raw = await asyncio.to_thread(retrieve_code, body.query, body.k)
    results = [RetrievedFunction(**r) for r in raw]
    retrieval_cache.set(f"{body.query}:{body.k}", results)
    return RetrieveResponse(results=results, cached=False)

@router.post("/generate", response_model=GenerateResponse)
@limiter.limit("10/minute")
async def generate(body: GenerateRequest, request: Request):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(status_code=503, detail="ANTHROPIC_API_KEY is not configured")

    cached = generation_cache.get(body.message)
    if cached is not None:
        return GenerateResponse(**cached, cached=True)

    from generate import generate_code
    result = await asyncio.to_thread(generate_code, body.message)

    retrieved = [RetrievedFunction(**r) for r in result["retrieved_functions"]]
    response_data = {
        "generated_code": result["generated_code"],
        "retrieved_functions": retrieved,
    }
    generation_cache.set(body.message, response_data)
    return GenerateResponse(**response_data, cached=False)
