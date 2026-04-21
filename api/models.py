from typing import Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    message: str


class RetrievedFunction(BaseModel):
    score: float
    function_name: str
    parameters: list[str]
    code: str


class GenerateResponse(BaseModel):
    generated_code: Optional[str] = None
    retrieved_functions: list[RetrievedFunction] = []
    cached: bool = False


class HealthResponse(BaseModel):
    status: str = "ok"
    retriever_loaded: bool = False
    provider_configured: bool = False


class RetrieveRequest(BaseModel):
    query: str
    k: int = Field(default=2, ge=1, le=10)


class RetrieveResponse(BaseModel):
    results: list[RetrievedFunction] = []
    cached: bool = False
