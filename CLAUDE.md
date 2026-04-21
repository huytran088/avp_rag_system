# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval-Augmented Generation) system for generating code in the AVP pseudocode language. It uses ANTLR4 to parse AVP source files, extracts function metadata into a knowledge base, and provides semantic code retrieval with reranking.

## Commands

**Regenerate ANTLR parser files from grammar:**
```bash
antlr4 -Dlanguage=Python3 -visitor Pseudocode.g4
```

**Ingest AVP files into knowledge base:**
```bash
uv run python ingest.py
```
This parses all `.avp` files in `./data/` and outputs `code_knowledge_base.json`.

**Run retrieval demo:**
```bash
uv run python retrieve.py
```

**Run generation demo:**
```bash
uv run python generate.py
```

**Start API server (development):**
```bash
uv run uvicorn api.main:app --reload
```

**Start frontend dev server:**
```bash
cd frontend && npm run dev
```

**Run Playwright E2E tests (requires running backend):**
```bash
cd frontend && npm run test:e2e
```

**Run unit tests:**
```bash
uv run pytest tests/ -v
```

**Docker (Anthropic-only):**
```bash
docker compose up --build
```

**Docker with vLLM sidecar (GPU required):**
```bash
docker compose --profile vllm up --build
```

**Deploy frontend to GitHub Pages (manual):**
```bash
cd frontend && VITE_BASE_PATH=/avp_rag_system/ VITE_API_BASE_URL=https://your-backend-url npm run deploy:gh-pages
```

## Architecture

### RAG Pipeline
1. **Ingest** (`ingest.py`): Uses ANTLR4 to parse `.avp` files, extracts function declarations via `CodeStructureVisitor`, outputs JSON knowledge base
2. **Retrieve** (`retrieve.py`): Two-stage retrieval using BGE embeddings + FAISS for fast vector search, optional BGE reranker for accuracy
3. **Generate** (`generate.py`): Builds prompts with retrieved code context, calls `providers.call_llm()` for generation

### LLM Providers (`providers.py`)
- `call_llm(prompt)`: Dispatches to configured provider with optional fallback
- `_call_anthropic()`: Anthropic Claude via `anthropic` SDK
- `_call_vllm()`: vLLM or Ollama via `openai` SDK (OpenAI-compatible API)
- `is_provider_configured()` / `get_provider_name()`: Used by API routes and CLI
- Controlled by env vars: `LLM_PROVIDER`, `LLM_FALLBACK_PROVIDER`

### REST API (`api/`)
- `api/main.py`: FastAPI app with CORS (configurable via `CORS_ORIGINS` env var), rate limiting, lifespan-based retriever init, static file serving
- `api/routes.py`: `/api/generate`, `/api/retrieve`, `/api/health` endpoints — uses `providers.py` for config checks
- `api/models.py`: Pydantic request/response schemas
- `api/cache.py`: TTL-based dict cache for retrieval and generation results
- `api/dependencies.py`: slowapi rate limiter instance

### Frontend (`frontend/`)
- React 19 + TypeScript + Tailwind CSS v4 + Vite
- `ChatPanel` component with configurable API URL (`VITE_API_BASE_URL` env var)
- Deployable to GitHub Pages (CI/CD in `.github/workflows/deploy-gh-pages.yml`)
- Playwright E2E tests in `frontend/e2e/`

### CI/CD (`.github/workflows/`)
- `ci.yml`: Backend pytest + frontend tsc + build on push/PR to `main`
- `deploy-gh-pages.yml`: Builds frontend with `VITE_BASE_PATH` and `VITE_API_BASE_URL`, deploys to GitHub Pages on push to `main`
- `sync-hf-spaces.yml`: Copies `hf-space/README.md` → `README.md`, force-pushes repo to HF Spaces on push to `main` — HF Spaces then builds `Dockerfile` and restarts

### ANTLR Components
- `Pseudocode.g4`: Grammar definition for the AVP language
- `PseudocodeLexer.py`, `PseudocodeParser.py`, `PseudocodeVisitor.py`: Generated parser files (regenerate after grammar changes)

### AVP Language Notes
- Python-like syntax with `fun`/`end fun`, `if`/`end if`, `for`/`end for`, `while`/`end while`
- Newlines are significant (statement separators)
- Strict 4-space indentation
- Keywords: `fun`, `for`, `in`, `if`, `else`, `while`, `return`, `break`, `end`, `and`, `or`, `True`, `False`
- Arrays: `[1, 2, 3]`, `[1 to 5]` (range), `(100)` (size)
- Comments: `// comment`

## Gotchas

- **Relative paths in API**: `api/` code must resolve paths via `Path(__file__).parent.parent` — knowledge base and data/ are at project root
- **Retriever init is slow (~30s)**: Uses BGE embedding + reranker model loading. API uses lifespan eager init to front-load this
- **slowapi requires `request: Request`** in route handler signatures even if unused — it inspects the parameter
- **ANTLR generated files are at project root**, not in a subdirectory — `PseudocodeLexer.py`, `PseudocodeParser.py`, `PseudocodeVisitor.py`
- **`tracking.py`**: Hash-based file change detection for incremental ingestion — imported by `ingest.py`
- **React 19 event types**: Named exports (`FormEvent`, `KeyboardEvent`) are deprecated — use `React.FormEvent` or structural types
- **Tailwind CSS v4**: Uses `@import "tailwindcss"` in CSS, no `tailwind.config.js`
- **`providers.py` reuses `vllm` provider for Ollama**: Ollama's OpenAI-compatible API at `:11434/v1` works with `_call_vllm()`. Set `VLLM_BASE_URL=http://localhost:11434/v1` and `VLLM_API_KEY=ollama`
- **`VITE_API_BASE_URL` is build-time only**: Vite inlines it during build. Changing it requires rebuilding the frontend, not just restarting
- **`CORS_ORIGINS` in `.env`**: Comma-separated extra origins appended to the default localhost origins in `api/main.py`. Restart backend after changing
- **`VITE_BASE_PATH`**: Set to `/avp_rag_system/` for GitHub Pages deployment (repo subpath). Defaults to `/` for local dev
- **`BrowserRouter basename`**: Must use `basename={import.meta.env.BASE_URL}` — without this, React Router can't match route `"/"` under the `/avp_rag_system/` subpath and the page renders blank
- **HF Spaces port**: HF Spaces requires port 7860. `Dockerfile` (backend-only) uses 7860; `Dockerfile.full` (docker compose) uses 8000
- **`hf-space/README.md`**: The HF Spaces YAML front matter lives here. `sync-hf-spaces.yml` copies it to `README.md` on the HF Spaces repo. Do not put HF Spaces metadata in the GitHub `README.md`
- **`uv sync --frozen`**: `Dockerfile` uses `--frozen` (requires `uv.lock`); `Dockerfile.full` omits it for flexibility during local compose builds

## API Details

- `POST /api/generate` (10/min) — calls `generate_code()` from `generate.py`, returns `{generated_code, retrieved_functions, cached}`
- `POST /api/retrieve` (30/min) — calls `retrieve_code()`, returns scored function matches
- `GET /api/health` — returns `{status, retriever_loaded, provider_configured}`
- TTL cache (1hr, 100 entries) for both retrieval and generation results
- `generate_code()` is the quiet core; `generate_solution()` is the CLI wrapper that prints
- Returns 503 when the active LLM provider is not configured, 429 on rate limit

## Docker

Two Dockerfiles:
- `Dockerfile` — backend-only image for Hugging Face Spaces (port 7860, `--frozen` uv install, no Node stage)
- `Dockerfile.full` — full-stack image for `docker compose` (Node builds frontend → Python runtime, port 8000)

`docker-compose.yml` explicitly points to `Dockerfile.full` via `build.dockerfile`.

Other notes:
- `static/` directory: built frontend copied here, served by FastAPI catch-all mount
- Knowledge base pre-generated during build (`RUN uv run python ingest.py`)
- Health check has 120s start period (model loading)
- `data/` volume-mounted for live .avp file updates
- vLLM sidecar via `profiles: [vllm]` — opt-in with `docker compose --profile vllm up`
- `depends_on: vllm` with `required: false` — avp-rag starts regardless of vLLM
- `huggingface_cache` named volume persists model weights across restarts
- See `docs/docker-deploy.md` for full deployment guide (HF Spaces, Ollama, tunnels)

## Debugging
Whenever you scan the project and found a bug, which could an error or an exception, don't try to fix it right away. Instead, create a test case suite in a separated folder (e.g. tests/), make sure that the code can pass all tests after fixing the bugs.

### Code Intelligence

Prefer LSP over Grep/Glob/Read for code navigation:
- `goToDefinition` / `goToImplementation` to jump to source
- `findReferences` to see all usages across the codebase
- `workspaceSymbol` to find where something is defined
- `documentSymbol` to list all symbols in a file
- `hover` for type info without reading the file
- `incomingCalls` / `outgoingCalls` for call hierarchy

Before renaming or changing a function signature, use
`findReferences` to find all call sites first.

Use Grep/Glob only for text/pattern searches (comments,
strings, config values) where LSP doesn't help.

After writing or editing code, check LSP diagnostics before
moving on. Fix any type errors or missing imports immediately.

