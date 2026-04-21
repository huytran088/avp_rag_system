# AVP Pseudocode RAG System

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg)

**Live demo:** [huytran088.github.io/avp_rag_system](https://huytran088.github.io/avp_rag_system/) &nbsp;|&nbsp; **API:** [beefstewbibi-avp-rag-system.hf.space](https://beefstewbibi-avp-rag-system.hf.space/api/health)

A Retrieval-Augmented Generation (RAG) system for the AVP pseudocode language. Uses ANTLR4 to parse AVP source files, extracts function metadata into a searchable knowledge base, and provides semantic code retrieval with optional reranking for LLM-powered code generation.

## Features

- **ANTLR4 Grammar** — Full parser for the AVP pseudocode language
- **Function Extraction** — Automatically extracts and indexes function declarations with metadata
- **Two-Stage Retrieval** — Fast vector search using BGE embeddings + FAISS, with optional BGE reranker for improved accuracy
- **Multi-Provider LLM** — Pluggable providers (Anthropic Claude, vLLM/OpenAI-compatible) with optional fallback
- **REST API** — FastAPI backend with rate limiting, TTL caching, and CORS support
- **React Chat UI** — Chat interface deployed to GitHub Pages
- **Fully Managed Deployment** — Backend on Hugging Face Spaces, frontend on GitHub Pages, both auto-deployed via GitHub Actions
- **Unit & E2E Tests** — pytest unit tests and Playwright end-to-end tests

## Architecture

### Deployed Architecture

```
GitHub Pages                              Hugging Face Spaces
huytran088.github.io/avp_rag_system       beefstewbibi-avp-rag-system.hf.space
  React SPA (BrowserRouter)      ──────►   FastAPI + BGE retrieval
  VITE_API_BASE_URL baked in               Anthropic Claude backend
  auto-deployed: deploy-gh-pages.yml       auto-deployed: sync-hf-spaces.yml
```

### RAG Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌────────────────────┐
│  .avp files │────▶│ ANTLR Parser │────▶│ JSON Knowledge Base│
└─────────────┘     └──────────────┘     └─────────┬──────────┘
                                                   │
                    ┌──────────────┐     ┌─────────▼──────────┐
                    │  LLM Prompt  │◀────│  Vector Retrieval  │
                    └──────┬───────┘     └────────────────────┘
                           │
              ┌────────────▼────────────┐
              │      providers.py       │
              │  Anthropic ◀──▶ vLLM    │
              └────────────┬────────────┘
                           │
                    ┌──────▼───────┐     ┌────────────────────┐
                    │  FastAPI /   │◀───▶│  React Chat UI     │
                    │  REST API    │     │  GitHub Pages       │
                    └──────────────┘     └────────────────────┘
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- ANTLR4 (only needed for grammar regeneration)
- Node.js 18+ (only needed for frontend development)

## Installation

```bash
git clone https://github.com/huytran088/avp_rag_system.git
cd avp_rag_system
uv sync
```

## Configuration

Copy the environment template and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | Active provider: `anthropic` or `vllm` |
| `LLM_FALLBACK_PROVIDER` | *(empty)* | Optional fallback provider on error |
| `ANTHROPIC_API_KEY` | — | Required when using the Anthropic provider |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-20250514` | Anthropic model to use |
| `VLLM_BASE_URL` | `http://vllm:8080/v1` | vLLM or Ollama OpenAI-compatible endpoint |
| `VLLM_MODEL` | `Qwen/Qwen3-8B` | Model served by vLLM/Ollama |
| `VLLM_API_KEY` | `token-placeholder` | API key for vLLM (Ollama ignores this) |
| `CORS_ORIGINS` | *(empty)* | Extra comma-separated origins beyond localhost |

## Usage

### 1. Ingest AVP Files

Parse all `.avp` files in the `data/` folder and build the knowledge base:

```bash
uv run python ingest.py
```

This creates `code_knowledge_base.json` with extracted function metadata.

### 2. Retrieve Code

Run the interactive retrieval demo:

```bash
uv run python retrieve.py
```

### 3. Generate Code

Run the RAG generation demo:

```bash
uv run python generate.py
```

### 4. Start the API Server

```bash
uv run uvicorn api.main:app --reload
```

Runs at `http://localhost:8000`. Endpoints:
- `GET /api/health`
- `POST /api/generate` (10 req/min)
- `POST /api/retrieve` (30 req/min)

### 5. Start the Frontend (development)

```bash
cd frontend && npm install && npm run dev
```

Opens at `http://localhost:5173` with API proxy to the backend.

## API Reference

Base URL (production): `https://beefstewbibi-avp-rag-system.hf.space`
Base URL (local dev): `http://localhost:8000`

---

### `GET /api/health`

Check backend status.

```bash
curl https://beefstewbibi-avp-rag-system.hf.space/api/health
```

```json
{
  "status": "ok",
  "retriever_loaded": true,
  "provider_configured": true
}
```

---

### `POST /api/generate`

Generate AVP pseudocode from a natural language description.

**Rate limit:** 10 requests/minute per IP

**Request:**
```json
{ "message": "write a function to find the maximum value in an array" }
```

**Response:**
```json
{
  "generated_code": "fun find_max(collection, size):\n    ...\nend fun",
  "retrieved_functions": [
    {
      "score": 1.59,
      "function_name": "max_value",
      "parameters": ["x", "y"],
      "code": "fun max_value(x, y):\n    ...\nend fun"
    }
  ],
  "cached": false
}
```

**curl:**
```bash
curl -X POST https://beefstewbibi-avp-rag-system.hf.space/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"message": "write a fibonacci function"}'
```

**Python:**
```python
import httpx

resp = httpx.post(
    "https://beefstewbibi-avp-rag-system.hf.space/api/generate",
    json={"message": "write a function to sort an array"},
)
resp.raise_for_status()
data = resp.json()
print(data["generated_code"])
```

**JavaScript/TypeScript:**
```ts
const res = await fetch(
  "https://beefstewbibi-avp-rag-system.hf.space/api/generate",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: "write a binary search function" }),
  },
);
const { generated_code, retrieved_functions } = await res.json();
```

---

### `POST /api/retrieve`

Search the knowledge base for relevant AVP functions without generating new code.

**Rate limit:** 30 requests/minute per IP

**Request:**
```json
{ "query": "sorting algorithm", "k": 3 }
```

| Field | Type | Default | Description |
|---|---|---|---|
| `query` | string | — | Natural language search query |
| `k` | integer | 5 | Number of results to return |

**Response:**
```json
[
  {
    "score": 1.45,
    "function_name": "bubble_sort",
    "parameters": ["collection", "size"],
    "code": "fun bubble_sort(collection, size):\n    ...\nend fun"
  }
]
```

**curl:**
```bash
curl -X POST https://beefstewbibi-avp-rag-system.hf.space/api/retrieve \
  -H 'Content-Type: application/json' \
  -d '{"query": "sorting algorithm", "k": 3}'
```

**Python:**
```python
import httpx

resp = httpx.post(
    "https://beefstewbibi-avp-rag-system.hf.space/api/retrieve",
    json={"query": "binary search", "k": 5},
)
results = resp.json()
for fn in results:
    print(f"{fn['function_name']} (score: {fn['score']:.2f})")
    print(fn["code"])
```

---

## Error Responses

| Status | Condition |
|---|---|
| `503 Service Unavailable` | LLM provider not configured (missing API key or unreachable endpoint) |
| `429 Too Many Requests` | Rate limit exceeded |
| `422 Unprocessable Entity` | Invalid request body |

---

## Integration Guide

### Using the API from an External Application

Point any HTTP client at the production base URL. No authentication is required.

**Minimal Python integration:**

```python
import httpx

BASE_URL = "https://beefstewbibi-avp-rag-system.hf.space"

def generate_avp(description: str) -> str:
    r = httpx.post(f"{BASE_URL}/api/generate", json={"message": description}, timeout=60)
    r.raise_for_status()
    return r.json()["generated_code"]

def search_avp(query: str, k: int = 5) -> list:
    r = httpx.post(f"{BASE_URL}/api/retrieve", json={"query": query, "k": k}, timeout=30)
    r.raise_for_status()
    return r.json()

# Example
code = generate_avp("write a function to compute the GCD of two numbers")
print(code)
```

**Minimal JavaScript integration:**

```ts
const BASE_URL = "https://beefstewbibi-avp-rag-system.hf.space";

async function generateAVP(description: string): Promise<string> {
  const res = await fetch(`${BASE_URL}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: description }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  const data = await res.json();
  return data.generated_code;
}
```

### Self-Hosting the Backend

If you need higher rate limits or a private deployment, run the backend yourself. See [docs/docker-deploy.md](docs/docker-deploy.md) for full instructions.

When self-hosting, set `CORS_ORIGINS` in the backend `.env` to allow your frontend's origin:
```
CORS_ORIGINS=https://your-frontend-domain.com
```

---

## Testing

### Unit Tests

```bash
uv run pytest tests/
```

Runs provider abstraction tests (mocked, no API keys needed).

### E2E Tests

```bash
cd frontend && npm run test:e2e
```

Requires the backend to be running with a configured LLM provider.

## Docker

### Full-Stack (docker compose, local dev)

Uses `Dockerfile.full` — builds the React frontend and serves it from the FastAPI backend.

```bash
cp .env.example .env  # Set ANTHROPIC_API_KEY
docker compose up --build
```

Served at `http://localhost:8000` with frontend at the root.

### Backend Only (Hugging Face Spaces)

`Dockerfile` is the backend-only image used by the HF Spaces deployment. It skips the Node build stage and listens on port 7860.

```bash
docker build -t avp-rag-backend .
docker run -p 7860:7860 \
  -e LLM_PROVIDER=anthropic \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  avp-rag-backend
```

### With Ollama + Qwen3 (local GPU)

```bash
ollama pull qwen3:8b
ollama serve
```

Then in `.env`:
```
LLM_PROVIDER=vllm
VLLM_BASE_URL=http://localhost:11434/v1
VLLM_MODEL=qwen3:8b
VLLM_API_KEY=ollama
```

### With vLLM (Docker, 16 GB+ VRAM)

```bash
docker compose --profile vllm up --build
```

## Deployment

See [docs/docker-deploy.md](docs/docker-deploy.md) for full deployment instructions:
- **Hugging Face Spaces** — recommended, fully managed, auto-deployed via GitHub Actions
- **Local + tunnel** — ngrok or Cloudflare Tunnel for local GPU servers

### CI/CD

Three GitHub Actions workflows:

| Workflow | Trigger | Action |
|---|---|---|
| `ci.yml` | push / PR to `main` | Backend pytest + frontend tsc + build |
| `deploy-gh-pages.yml` | push to `main` | Builds frontend with `VITE_API_BASE_URL`, deploys to GitHub Pages |
| `sync-hf-spaces.yml` | push to `main` | Force-pushes repo to HF Spaces (triggers Docker build) |

### Required Secrets and Variables

**GitHub repo** (Settings → Secrets and variables → Actions):

| Name | Type | Value |
|---|---|---|
| `HF_TOKEN` | Secret | Hugging Face write-access token |
| `VITE_API_BASE_URL` | Variable | `https://beefstewbibi-avp-rag-system.hf.space` |

**Hugging Face Space** (Space Settings):

| Name | Type | Value |
|---|---|---|
| `ANTHROPIC_API_KEY` | Secret | Your Anthropic API key |
| `LLM_PROVIDER` | Variable | `anthropic` |
| `CORS_ORIGINS` | Variable | `https://huytran088.github.io` |

## Project Structure

```
├── Pseudocode.g4            # ANTLR4 grammar definition
├── PseudocodeLexer.py       # Generated lexer
├── PseudocodeParser.py      # Generated parser
├── PseudocodeVisitor.py     # Generated visitor
├── ingest.py                # Parses AVP files, builds knowledge base
├── retrieve.py              # Two-stage semantic retrieval
├── generate.py              # RAG prompt generation
├── providers.py             # Multi-provider LLM abstraction (Anthropic, vLLM)
├── tracking.py              # Hash-based incremental file tracking
├── api/                     # FastAPI REST API
│   ├── main.py              # App setup, CORS, static files
│   ├── routes.py            # /health, /retrieve, /generate endpoints
│   ├── models.py            # Pydantic schemas
│   ├── cache.py             # TTL cache (retrieval + generation)
│   └── dependencies.py      # Rate limiter config
├── frontend/                # React + TypeScript chat UI
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatPanel.tsx  # Main chat interface
│   │   ├── main.tsx         # React entry + routing (BrowserRouter w/ basename)
│   │   └── App.tsx          # Root component
│   ├── e2e/
│   │   └── chat.spec.ts     # Playwright E2E tests
│   └── vite.config.ts       # Vite + API proxy config
├── tests/                   # Unit tests
│   └── test_providers.py    # Provider abstraction tests
├── data/                    # Sample AVP source files
│   ├── algorithms.avp
│   ├── array_ops.avp
│   ├── logic.avp
│   └── math_utils.avp
├── .github/workflows/
│   ├── ci.yml               # Tests on push/PR
│   ├── deploy-gh-pages.yml  # Frontend deploy to GitHub Pages
│   └── sync-hf-spaces.yml   # Backend deploy to Hugging Face Spaces
├── docs/
│   └── docker-deploy.md     # Full deployment guide
├── hf-space/
│   └── README.md            # HF Spaces YAML metadata (copied to root by sync workflow)
├── Dockerfile               # Backend-only image (HF Spaces, port 7860)
├── Dockerfile.full          # Full-stack image (docker compose, port 8000)
├── docker-compose.yml       # Local full-stack deployment
├── .env.example             # Environment variable template
└── PseudocodeSyntax.md      # AVP language reference
```

## AVP Language

AVP is a Python-like pseudocode language designed for algorithm visualization. Example:

```
fun factorial(n):
    if (n <= 1):
        return 1
    end if
    return n * factorial(n - 1)
end fun
```

See [PseudocodeSyntax.md](PseudocodeSyntax.md) for the full language reference.

## License

MIT
