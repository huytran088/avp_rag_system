# AVP Pseudocode RAG System

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg)

A Retrieval-Augmented Generation (RAG) system for the AVP pseudocode language. Uses ANTLR4 to parse AVP source files, extracts function metadata into a searchable knowledge base, and provides semantic code retrieval with optional reranking for LLM-powered code generation.

## Features

- **ANTLR4 Grammar** — Full parser for the AVP pseudocode language
- **Function Extraction** — Automatically extracts and indexes function declarations with metadata
- **Two-Stage Retrieval** — Fast vector search using BGE embeddings + FAISS, with optional BGE reranker for improved accuracy
- **Multi-Provider LLM** — Pluggable providers (Anthropic Claude, vLLM/OpenAI-compatible) with optional fallback
- **REST API** — FastAPI backend with rate limiting and caching
- **React Chat UI** — Chat interface for testing the API locally
- **Docker** — Multi-stage build with optional GPU-accelerated vLLM sidecar
- **Unit & E2E Tests** — pytest unit tests and Playwright end-to-end tests

## Architecture

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
                    │  REST API    │     │  (localhost:5173)   │
                    └──────────────┘     └────────────────────┘
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- ANTLR4 (only needed for grammar regeneration)
- Node.js 18+ (only needed for frontend development)

## Installation

```bash
git clone <repository-url>
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
| `VLLM_BASE_URL` | `http://vllm:8080/v1` | vLLM OpenAI-compatible endpoint |
| `VLLM_MODEL` | `Qwen/Qwen3-8B` | Model served by vLLM |
| `VLLM_API_KEY` | `token-placeholder` | API key for vLLM (if authentication is enabled) |

## Usage

### 1. Ingest AVP Files

Parse all `.avp` files in the `data/` folder and build the knowledge base:

```bash
uv run python ingest.py
```

This creates `code_knowledge_base.json` with extracted function metadata.

### 2. Retrieve Code

Run the interactive retrieval demo to search for relevant code snippets:

```bash
uv run python retrieve.py
```

### 3. Generate Code

Run the RAG generation demo to create new AVP code based on natural language queries:

```bash
uv run python generate.py
```

### 4. Start the API Server

```bash
uv run uvicorn api.main:app --reload
```

The API runs at `http://localhost:8000`. Endpoints:
- `GET /api/health` — status check (provider status)
- `POST /api/generate` — generate AVP code from natural language (10 req/min)
- `POST /api/retrieve` — search the knowledge base (30 req/min)

### 5. Start the Frontend (development)

```bash
cd frontend && npm install && npm run dev
```

Opens at `http://localhost:5173` with API proxy to the backend.

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

### Anthropic-only (default)

```bash
cp .env.example .env  # Set ANTHROPIC_API_KEY
docker compose up --build
```

The app is served at `http://localhost:8000` with the frontend built into FastAPI's static file serving.

### With Ollama + Qwen3 (local GPU, recommended)

```bash
ollama pull qwen3:8b
ollama serve
```

Then set in `.env`:
```
LLM_PROVIDER=vllm
VLLM_BASE_URL=http://localhost:11434/v1
VLLM_MODEL=qwen3:8b
```

Ollama auto-quantizes models to fit your GPU. Works on consumer cards (RTX 3060+).

### With vLLM + Qwen3 (Docker, full precision)

```bash
docker compose --profile vllm up --build
```

Requires an NVIDIA GPU with 16 GB+ VRAM and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html). First startup downloads ~16 GB of model weights (cached in a Docker volume).

### Regenerate Parser (after grammar changes)

```bash
antlr4 -Dlanguage=Python3 -visitor Pseudocode.g4
```

## Deployment

See [docs/docker-deploy.md](docs/docker-deploy.md) for detailed deployment instructions covering:
- Local backend with Ollama or vLLM serving Qwen3 models
- Exposing your local backend via ngrok or Cloudflare Tunnel
- Frontend auto-deployed to GitHub Pages via CI/CD
- CORS, environment variables, and production checklist

### CI/CD

Two GitHub Actions workflows are included:
- **CI** (`.github/workflows/ci.yml`) — runs backend unit tests and frontend type check + build on every push/PR
- **Deploy** (`.github/workflows/deploy-gh-pages.yml`) — builds and deploys frontend to GitHub Pages on push to `main`

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
│   │   ├── main.tsx         # React entry + routing
│   │   └── App.tsx          # Root component
│   ├── e2e/
│   │   └── chat.spec.ts    # Playwright E2E tests
│   └── vite.config.ts      # Vite + API proxy config
├── tests/                   # Unit tests
│   └── test_providers.py    # Provider abstraction tests
├── data/                    # Sample AVP source files
│   ├── algorithms.avp
│   ├── array_ops.avp
│   ├── logic.avp
│   └── math_utils.avp
├── .github/workflows/       # CI/CD
│   ├── ci.yml               # Tests on push/PR
│   └── deploy-gh-pages.yml  # Frontend deploy to GitHub Pages
├── docs/
│   └── docker-deploy.md     # Full deployment guide
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Deployment (with optional vLLM profile)
├── .env.example             # Environment variable template
└── PseudocodeSyntax.md      # AVP language reference
```

## API Reference

### `POST /api/generate`
Generate AVP code from a natural language description.
```bash
curl -X POST http://localhost:8000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"message": "write a fibonacci function"}'
```
Response: `{ "generated_code": "...", "retrieved_functions": [...], "cached": false }`

### `POST /api/retrieve`
Search the knowledge base for relevant code snippets.
```bash
curl -X POST http://localhost:8000/api/retrieve \
  -H 'Content-Type: application/json' \
  -d '{"query": "sorting algorithm", "k": 3}'
```

### `GET /api/health`
Check backend status.
```bash
curl http://localhost:8000/api/health
```
Response: `{ "status": "ok", "retriever_loaded": true, "provider_configured": true }`

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
