# AVP Pseudocode RAG System

![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green.svg)

**Frontend demo (AVP app):** [huytran088.github.io/avp](https://huytran088.github.io/avp/) — the [Algorithm Visualization Project](https://github.com/huytran088/algorithm-visualization-project), whose AI pane is powered by this backend<br>
**Chat UI:** [huytran088.github.io/avp_rag_system](https://huytran088.github.io/avp_rag_system/) &nbsp;|&nbsp; **API:** [beefstewbibi-avp-rag-system.hf.space](https://beefstewbibi-avp-rag-system.hf.space/api/health)

A Retrieval-Augmented Generation (RAG) system for the AVP pseudocode language. It uses ANTLR4 to parse AVP source files, extracts function metadata into a searchable knowledge base, retrieves the most relevant examples with BGE embeddings + FAISS (plus an optional cross-encoder reranker), and prompts an LLM to write new AVP code in the same style.

## Features

- **ANTLR4 Grammar**: full parser for the AVP pseudocode language (`avp_rag/parser/Pseudocode.g4`)
- **Incremental Ingestion**: hash-based change tracking, so only new or modified `.avp` files are re-parsed
- **Two-Stage Retrieval**: BGE embeddings + FAISS cosine search, then an optional BGE cross-encoder rerank
- **Multi-Provider LLM**: Anthropic Claude, vLLM/Ollama (OpenAI-compatible), Hugging Face Inference Providers and Google Gemini, with an optional fallback provider
- **REST API**: FastAPI backend with rate limiting, TTL caching and configurable CORS
- **Two Frontends**: the AVP visualization app (AI pane) and a standalone React chat UI on GitHub Pages
- **Automated Deployment**: backend on Hugging Face Spaces, frontend on GitHub Pages, both via GitHub Actions
- **Unit & E2E Tests**: pytest for the backend, Playwright (mocked and live) for the chat UI

## Architecture

### Deployed Architecture

```
Frontends (GitHub Pages)                      Backend (HF Spaces, Docker :7860)
─────────────────────────                     ─────────────────────────────────
huytran088.github.io/avp            ──POST──▶  FastAPI  /api/generate
  AVP visualization app (AI pane)                       /api/retrieve
                                                        /api/health
huytran088.github.io/avp_rag_system ──POST──▶     │
  React chat UI (frontend/)                       ▼
                                               BGE + FAISS retrieval + reranker
                                                  │
                                                  ▼
                                               providers.call_llm()
                                                 HF router (Qwen3-Coder)
                                                 └─ fallback: Gemini
```

The same backend can also run on a self-hosted GPU server with a local vLLM model (e.g. Qwen3.6-27B AWQ) as the primary provider and a hosted API as fallback. See `.env.example` and [docs/docker-deploy.md](docs/docker-deploy.md).

### RAG Pipeline

```
┌─────────────┐   ┌──────────────────────┐   ┌──────────────────────────┐
│ data/*.avp  │──▶│ ANTLR4 parser +      │──▶│ code_knowledge_base.json │
└─────────────┘   │ CodeStructureVisitor │   │ {metadata, chunks}       │
                  └──────────────────────┘   └────────────┬─────────────┘
        1. INGEST  (avp_rag/ingest.py, tracking.py)       │
                                                          ▼
┌────────────────────────────────────────────────────────────────────┐
│ 2. RETRIEVE (avp_rag/retrieve.py)                                  │
│  query ─▶ BGE embed (bge-base-en-v1.5) ─▶ FAISS IndexFlatIP, k×3   │
│        ─▶ BGE reranker (bge-reranker-base) ─▶ top k functions      │
└───────────────────────────────┬────────────────────────────────────┘
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│ 3. GENERATE (avp_rag/generate.py)                                  │
│  build_context(): retrieved snippets + AVP rules ─▶ prompt         │
│  generate_code(): providers.call_llm(prompt)                       │
│     LLM_PROVIDER ─(on error)─▶ LLM_FALLBACK_PROVIDER               │
│     anthropic | vllm (vLLM/Ollama) | hf | gemini                   │
└────────────────────────────────────────────────────────────────────┘
```

1. **Ingest**: `run_ingest()` hashes each `.avp` file in `data/`, re-parses only changed files, extracts every function declaration (name, parameters, full source text, source file, plus the file title and the `//` comment directly above the function) and saves the knowledge base with tracking metadata. Deleted files are pruned, and a knowledge base from an older format (`kb_format`) is rebuilt.
2. **Retrieve**: `CodeRetriever` embeds `"<title>: <description>\nFunction: name(params)\n<code>"` for every function (the reranker scores the same text), L2-normalizes the vectors and indexes them in FAISS. A query fetches `k × 3` candidates, which the cross-encoder reranks down to `k`. Models run on `EMBEDDING_DEVICE` (default `cpu`; fp16 on `cuda`). Queries are serialized with a lock, because HF fast tokenizers are not thread-safe.
3. **Generate**: `build_context()` retrieves once (default `k=2`) and builds a prompt with the reference code and AVP syntax rules. `generate_code()` sends it to the configured provider. Qwen-style `<think>` blocks are stripped from the output.

### Python Package (`avp_rag/`)

| Module | Role |
|---|---|
| `config.py` | Absolute paths (`PROJECT_ROOT`, `DATA_DIR`, `KB_PATH`, `STATIC_DIR`, `ENV_FILE`) and model defaults |
| `knowledge_base.py` | `load_kb()` / `save_kb()`: reads legacy (list) and tracked (`{metadata, chunks}`) formats |
| `tracking.py` | SHA-256 change detection; files keyed relative to `PROJECT_ROOT` (e.g. `data/foo.avp`) |
| `ingest.py` | `CodeStructureVisitor`, `parse_file()`, `run_ingest()` → `IngestResult` |
| `retrieve.py` | `CodeRetriever`, `retrieve_code()`, lazily-created global retriever |
| `generate.py` | `build_prompt()`, `build_context()`, `generate_code()`, CLI `generate_solution()` |
| `providers.py` | `call_llm()` with fallback, `is_provider_configured()`, `get_provider_name()` |
| `parser/` | `Pseudocode.g4` + generated lexer/parser/visitor |

The root `ingest.py`, `retrieve.py` and `generate.py` are thin shims; `uv run python -m avp_rag.<module>` is equivalent.

## Requirements

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js **20+** (`.nvmrc` pins 24.16.0; CI uses 20), only for the chat UI frontend
- Java + network access on first run, only to regenerate the ANTLR parser (`antlr4-tools`)
- Optional: an NVIDIA GPU for faster embeddings (`EMBEDDING_DEVICE=cuda`) or for serving vLLM

### Python Dependencies (`pyproject.toml`)

| Package | Purpose |
|---|---|
| `antlr4-python3-runtime>=4.13.2` | Runtime for the generated AVP parser |
| `flagembedding>=1.3.5` | BGE embedding model and reranker (`FlagModel`, `FlagReranker`) |
| `sentence-transformers>=3.3,<4`, `transformers>=4.44,<5`, `torch>=2.9.1` | Model backends for FlagEmbedding |
| `faiss-cpu>=1.13.1`, `numpy>=2.3.5` | Vector index and math |
| `anthropic>=0.42.0` | Anthropic Claude provider |
| `openai>=1.0,<2` | vLLM / Ollama / HF router / Gemini (OpenAI-compatible) providers |
| `fastapi>=0.115.0`, `uvicorn[standard]>=0.34.0` | REST API server |
| `slowapi>=0.1.9` | Rate limiting |
| `python-dotenv>=1.1.0` | Loads `.env` |

**Dev group:** `antlr4-tools>=0.2.2` (parser generation), `httpx>=0.28.0` (API tests), `pytest>=9.0.3`.

### Frontend Dependencies (`frontend/package.json`)

React 19, React Router 7, Tailwind CSS v4 (`@tailwindcss/vite`), Vite 6, TypeScript 5.8, Playwright and `gh-pages`.

## Installation

```bash
git clone https://github.com/huytran088/avp_rag_system.git
cd avp_rag_system
uv sync            # add --dev for tests and parser tooling
```

The first retriever start downloads the BGE models from Hugging Face (~30 s load time afterwards).

## Configuration

```bash
cp .env.example .env
```

| Variable | Default (in code) | Description |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | Active provider: `anthropic`, `vllm`, `hf` or `gemini` |
| `LLM_FALLBACK_PROVIDER` | *(empty)* | Provider tried if the primary raises |
| `ANTHROPIC_API_KEY` | — | Required for `anthropic` |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-20250514` | Anthropic model |
| `VLLM_BASE_URL` | `http://localhost:8001/v1` | vLLM or Ollama (`http://localhost:11434/v1`) endpoint; required for `vllm` |
| `VLLM_MODEL` | `qwen3.6-27b-awq` | Must match vLLM's `--served-model-name` |
| `VLLM_API_KEY` | `token-placeholder` | API key (Ollama ignores it) |
| `VLLM_ENABLE_THINKING` | `false` | Keep Qwen `<think>` reasoning in the output |
| `VLLM_TEMPERATURE` / `VLLM_TOP_P` / `VLLM_TOP_K` / `VLLM_MAX_TOKENS` | `0.6` / `0.95` / `20` / `1024` | vLLM sampling |
| `HF_TOKEN` | — | Required for `hf` (Hugging Face Inference Providers router) |
| `HF_MODEL` | `Qwen/Qwen3-Coder-30B-A3B-Instruct:cheapest` | `:cheapest` / `:fastest` lets the router pick a provider |
| `GEMINI_API_KEY` | — | Required for `gemini` |
| `GEMINI_MODEL` | `gemini-flash-lite-latest` | Gemini model (OpenAI-compatible endpoint) |
| `LLM_MAX_TOKENS` / `LLM_TEMPERATURE` | `1024` / `0.6` | Sampling for `hf` and `gemini` |
| `EMBEDDING_DEVICE` | `cpu` | Device for embedding + reranker models (`cpu` or `cuda`) |
| `CORS_ORIGINS` | *(empty)* | Extra comma-separated origins added to `localhost:5173` and `localhost:3000` |
| `RATE_LIMIT_IP_SOURCE` | `x-real-ip` | Where the per-client rate limit gets the client address: `x-real-ip` (a proxy that overwrites it, like the capstone nginx), `x-forwarded-for` (HF Spaces; set in `Dockerfile`) or `peer` (socket address). Only use a header your proxy sets, or clients can forge it |
| `FORWARDED_TRUSTED_HOPS` | `1` | With `x-forwarded-for`: which entry to use, counted from the right (the entries a client can forge are on the left) |

## Usage

### 1. Ingest AVP Files

```bash
uv run python ingest.py
```

Parses every `.avp` file in `data/` and writes `code_knowledge_base.json` at the project root (works from any cwd). Re-running only re-parses changed files.

### 2. Retrieve Code (interactive demo)

```bash
uv run python retrieve.py
```

### 3. Generate Code (interactive demo)

```bash
uv run python generate.py
```

Prints the full prompt, then the generated code. If the provider isn't configured it runs in simulation mode and only shows the prompt.

### 4. Start the API Server

```bash
uv run uvicorn api.main:app --reload
```

Runs at `http://localhost:8000`. The retriever loads eagerly at startup. If `static/` exists, the built frontend is served at `/`.

### 5. Start the Chat UI (development)

```bash
cd frontend && npm install && npm run dev
```

Opens at `http://localhost:5173` with an API proxy to the backend.

### 6. Regenerate the Parser (after grammar changes)

```bash
cd avp_rag/parser && uv run antlr4 -v 4.13.2 -Dlanguage=Python3 -visitor -no-listener Pseudocode.g4
```

## API Reference

Base URL (production): `https://beefstewbibi-avp-rag-system.hf.space`
Base URL (local dev): `http://localhost:8000`

No authentication. Results are cached for 1 hour (100 entries; keys are trimmed and lower-cased).

### `GET /api/health`

```bash
curl https://beefstewbibi-avp-rag-system.hf.space/api/health
```

```json
{ "status": "ok", "retriever_loaded": true, "provider_configured": true }
```

### `POST /api/generate`

Generate AVP pseudocode from a natural language description. **Rate limit:** 10 requests/minute per IP.

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string (1–2000 chars) | yes | The user's request. Used for retrieval and as the prompt's `TASK` |
| `code` | string (≤ 20000 chars) | no | Current editor code. Added to the prompt and to the retrieval search |
| `instructions` | string (≤ 8000 chars) | no | Extra language rules from the client. Added to the prompt only, never searched |

The cache key covers all three fields.

**Request:**
```json
{ "query": "write a function to find the maximum value in an array" }
```

**Request with editor context** (as sent by the [AVP app](https://huytran088.github.io/avp/)):
```json
{
  "query": "make it sort in descending order",
  "code": "fun Bubble_Sort(array):\n    ...\nend fun",
  "instructions": "All function names must start with a capital letter."
}
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

```bash
curl -X POST https://beefstewbibi-avp-rag-system.hf.space/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"query": "write a fibonacci function"}'
```

### `POST /api/retrieve`

Search the knowledge base without generating code. **Rate limit:** 30 requests/minute per IP.

| Field | Type | Default | Description |
|---|---|---|---|
| `query` | string | — | Natural language search query |
| `k` | integer | `2` | Number of results (1–10) |

**Request:**
```json
{ "query": "sorting algorithm", "k": 3 }
```

**Response:**
```json
{
  "results": [
    {
      "score": 1.45,
      "function_name": "bubble_sort",
      "parameters": ["collection", "size"],
      "code": "fun bubble_sort(collection, size):\n    ...\nend fun"
    }
  ],
  "cached": false
}
```

Scores are reranker logits when the reranker is enabled, cosine similarities otherwise.

### Error Responses

| Status | Condition |
|---|---|
| `503 Service Unavailable` | Active LLM provider not configured (missing key / base URL) |
| `429 Too Many Requests` | Rate limit exceeded |
| `422 Unprocessable Entity` | Invalid request body (e.g. missing `query`, `k` out of range) |

## Integration

**Python:**
```python
import httpx

BASE_URL = "https://beefstewbibi-avp-rag-system.hf.space"

def generate_avp(query: str) -> str:
    r = httpx.post(f"{BASE_URL}/api/generate", json={"query": query}, timeout=60)
    r.raise_for_status()
    return r.json()["generated_code"]

def search_avp(query: str, k: int = 3) -> list[dict]:
    r = httpx.post(f"{BASE_URL}/api/retrieve", json={"query": query, "k": k}, timeout=30)
    r.raise_for_status()
    return r.json()["results"]

print(generate_avp("write a function to compute the GCD of two numbers"))
```

**TypeScript:**
```ts
const BASE_URL = "https://beefstewbibi-avp-rag-system.hf.space";

async function generateAVP(query: string): Promise<string> {
  const res = await fetch(`${BASE_URL}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return (await res.json()).generated_code;
}
```

When self-hosting for another frontend, add its origin to `CORS_ORIGINS` in the backend `.env` and restart.

## Testing

```bash
uv run pytest tests/ -v          # backend unit + API tests (mocked, no keys or models needed)
cd frontend && npm run test:e2e:ci   # Playwright, mocked backend (what CI runs)
cd frontend && npm run test:e2e      # Playwright against a running backend
```

## Docker

| File | Use | Port |
|---|---|---|
| `Dockerfile` | Backend-only image for Hugging Face Spaces (`uv sync --frozen`, no Node stage) | 7860 |
| `Dockerfile.full` | Full stack for `docker compose`: Node builds the chat UI, FastAPI serves it from `static/` | 8000 |

Both images pre-build the knowledge base at build time and include a health check with a 120 s start period.

```bash
# Full stack
cp .env.example .env
docker compose up --build                     # http://localhost:8000

# Full stack + vLLM sidecar (GPU, serves Qwen/Qwen3-8B on :8080)
docker compose --profile vllm up --build

# Backend only
docker build -t avp-rag-backend .
docker run -p 7860:7860 -e LLM_PROVIDER=hf -e HF_TOKEN=hf_... avp-rag-backend
```

**Ollama (local GPU):**
```bash
ollama pull qwen3.6:27b && ollama serve
```
```
LLM_PROVIDER=vllm
VLLM_BASE_URL=http://localhost:11434/v1
VLLM_MODEL=qwen3.6:27b
VLLM_API_KEY=ollama
```

## Deployment

See [docs/docker-deploy.md](docs/docker-deploy.md) for the full guide (HF Spaces, Ollama, nginx / Cloudflare Tunnel).

### CI/CD

| Workflow | Trigger | Action |
|---|---|---|
| `ci.yml` | push / PR to `main` | Backend pytest, frontend `tsc` + build, mocked Playwright E2E |
| `deploy-gh-pages.yml` | push to `main` | Builds the chat UI with `VITE_BASE_PATH=/avp_rag_system/` and `VITE_API_BASE_URL`, deploys to GitHub Pages |
| `sync-hf-spaces.yml` | push to `main` | Copies `hf-space/README.md` → `README.md` and force-pushes to HF Spaces, which rebuilds `Dockerfile` |

### Secrets and Variables

**GitHub repo** (Settings → Secrets and variables → Actions):

| Name | Type | Value |
|---|---|---|
| `HF_TOKEN` | Secret | Hugging Face write-access token |
| `VITE_API_BASE_URL` | Variable | `https://beefstewbibi-avp-rag-system.hf.space` |

**Hugging Face Space** (Space Settings):

| Name | Type | Value |
|---|---|---|
| `HF_TOKEN` | Secret | Token billed for HF Inference Providers |
| `GEMINI_API_KEY` | Secret | Fallback provider key |
| `LLM_PROVIDER` | Variable | `hf` |
| `LLM_FALLBACK_PROVIDER` | Variable | `gemini` |
| `CORS_ORIGINS` | Variable | `https://huytran088.github.io` |

## Project Structure

```
├── avp_rag/                 # Core Python package (see table above)
│   └── parser/              # Pseudocode.g4 + generated lexer/parser/visitor
├── ingest.py, retrieve.py, generate.py   # Thin CLI shims
├── api/                     # FastAPI app
│   ├── main.py              # Lifespan retriever init, CORS, rate limiter, static mount
│   ├── routes.py            # /api/health, /api/retrieve, /api/generate
│   ├── models.py            # Pydantic schemas
│   ├── cache.py             # TTL cache (retrieval + generation)
│   └── dependencies.py      # slowapi limiter
├── frontend/                # React chat UI (Vite + Tailwind v4)
│   ├── src/                 # api/client.ts, hooks/useChat.ts, components/, types.ts
│   └── e2e/                 # chat.spec.ts (live), chat-mocked.spec.ts (CI)
├── tests/                   # pytest suite
├── data/                    # AVP knowledge source (12 files: sorts, searches, partitions, math, logic, arrays)
├── docs/                    # docker-deploy.md, PseudocodeSyntax.md
├── hf-space/README.md       # HF Spaces YAML front matter
├── Dockerfile, Dockerfile.full, docker-compose.yml
├── .env.example
└── .github/workflows/       # ci.yml, deploy-gh-pages.yml, sync-hf-spaces.yml
```

## AVP Language

AVP is a Python-like pseudocode language for algorithm visualization, used by the [AVP app](https://huytran088.github.io/avp/). Example:

```
fun factorial(n):
    if (n <= 1):
        return 1
    end if
    return n * factorial(n - 1)
end fun
```

See [docs/PseudocodeSyntax.md](docs/PseudocodeSyntax.md) for the full reference.

## License

MIT
