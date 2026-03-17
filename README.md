# AVP Pseudocode RAG System

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg)

A Retrieval-Augmented Generation (RAG) system for the AVP pseudocode language. Uses ANTLR4 to parse AVP source files, extracts function metadata into a searchable knowledge base, and provides semantic code retrieval with optional reranking for LLM-powered code generation.

## Features

- **ANTLR4 Grammar** - Full parser for the AVP pseudocode language
- **Function Extraction** - Automatically extracts and indexes function declarations with metadata
- **Two-Stage Retrieval** - Fast vector search using BGE embeddings + FAISS, with optional BGE reranker for improved accuracy
- **RAG Generation** - Builds context-aware prompts for LLM code generation
- **REST API** - FastAPI backend with rate limiting and caching
- **React Chat UI** - Barebone chat interface for testing the API locally
- **Docker** - Multi-stage build for one-command deployment

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
                    ┌──────▼───────┐     ┌────────────────────┐
                    │  FastAPI /   │◀───▶│  React Chat UI     │
                    │  REST API    │     │  (localhost:5173)   │
                    └──────────────┘     └────────────────────┘
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- ANTLR4 (only needed for grammar regeneration)

## Installation

```bash
git clone <repository-url>
cd antlr4_tut
uv sync
```

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
- `GET /api/health` — status check
- `POST /api/generate` — generate AVP code from natural language (10 req/min)
- `POST /api/retrieve` — search the knowledge base (30 req/min)

### 5. Start the Frontend (development)

```bash
cd frontend && npm install && npm run dev
```

Opens at `http://localhost:5173` with API proxy to the backend.

### 6. Run E2E Tests

```bash
cd frontend && npm run test:e2e
```

Requires the backend to be running with a valid `ANTHROPIC_API_KEY`.

### Docker (one-command deployment)

```bash
cp .env.example .env  # Add your ANTHROPIC_API_KEY
docker compose up --build
```

Opens at `http://localhost:8000` with the frontend served by FastAPI.

### Regenerate Parser (after grammar changes)

```bash
antlr4 -Dlanguage=Python3 -visitor Pseudocode.g4
```

## Project Structure

```
├── Pseudocode.g4            # ANTLR4 grammar definition
├── PseudocodeLexer.py       # Generated lexer
├── PseudocodeParser.py      # Generated parser
├── PseudocodeVisitor.py     # Generated visitor
├── ingest.py                # Parses AVP files, builds knowledge base
├── retrieve.py              # Two-stage semantic retrieval
├── generate.py              # RAG prompt generation
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
├── data/                    # Sample AVP source files
│   ├── algorithms.avp
│   ├── array_ops.avp
│   ├── logic.avp
│   └── math_utils.avp
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # One-command deployment
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
Response: `{ "status": "ok", "retriever_loaded": true, "api_key_configured": true }`

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
