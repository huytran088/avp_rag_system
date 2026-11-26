from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    # The user's request; used (with `code`) for retrieval
    query: str = Field(min_length=1, max_length=2000)
    # Current editor code the request may refer to
    code: str | None = Field(default=None, max_length=20000)
    # Extra client-side language rules; added to the prompt, never embedded
    instructions: str | None = Field(default=None, max_length=8000)


class RetrievedFunction(BaseModel):
    score: float
    function_name: str
    parameters: list[str]
    code: str


class GenerateResponse(BaseModel):
    generated_code: str | None = None
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
