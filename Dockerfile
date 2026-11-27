FROM python:3.12-slim
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

COPY avp_rag/ ./avp_rag/
COPY ingest.py ./
COPY api/ ./api/
COPY data/ ./data/

RUN uv run python ingest.py

# HF Spaces: every request comes through HF's proxy, which appends the client
# address to X-Forwarded-For. Key the rate limit on that entry (not the proxy's
# address, which would put all users in one bucket, nor X-Real-IP, which
# HF doesn't set and a client could forge). The server logs the header's entry
# count once; raise FORWARDED_TRUSTED_HOPS if HF adds more hops after it.
ENV RATE_LIMIT_IP_SOURCE=x-forwarded-for \
    FORWARDED_TRUSTED_HOPS=1

EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/api/health')" || exit 1

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
