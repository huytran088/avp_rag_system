"""Shared fixtures for API integration tests."""

import os
from unittest.mock import MagicMock, patch

import pytest
from starlette.testclient import TestClient


MOCK_RETRIEVE_RESULT = [
    {
        "score": 0.95,
        "function_name": "addNumbers",
        "parameters": ["a", "b"],
        "code": "fun addNumbers(a, b):\n    return a + b\nend fun",
    }
]

MOCK_LLM_OUTPUT = "fun mock():\n    return 1\nend fun"


@pytest.fixture()
def client():
    """TestClient with mocked retriever, LLM, and env vars.

    The retriever is pre-set so the lifespan's get_retriever() short-circuits,
    avoiding heavy ML model loading.
    """
    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = MOCK_RETRIEVE_RESULT

    env = {
        "ANTHROPIC_API_KEY": "fake-key-for-testing",
        "LLM_PROVIDER": "anthropic",
    }

    with (
        patch("retrieve._retriever", mock_retriever),
        patch("generate.call_llm", return_value=MOCK_LLM_OUTPUT),
        patch.dict(os.environ, env),
    ):
        from api.main import app
        from api.dependencies import limiter as original_limiter

        # Reset the original limiter's counters — the @limiter.limit() decorators
        # captured this instance at import time, so replacing app.state.limiter
        # alone is not enough.
        original_limiter.reset()

        from api.cache import generation_cache, retrieval_cache

        generation_cache.clear()
        retrieval_cache.clear()

        with TestClient(app) as c:
            yield c

        generation_cache.clear()
        retrieval_cache.clear()
