# Deployment Guide

This guide covers all deployment options for the AVP RAG system.

## Recommended: Hugging Face Spaces + GitHub Pages

The production deployment uses fully managed hosting with no tunnels or local servers required:

```
GitHub Pages                              Hugging Face Spaces
huytran088.github.io/avp_rag_system       beefstewbibi-avp-rag-system.hf.space
  React SPA (static)              ──────►   FastAPI + BGE + Anthropic
  auto-deployed via CI/CD                   auto-deployed via CI/CD
```

Both are auto-deployed on every push to `main`. See [One-Time Setup](#one-time-setup) to configure secrets.

---

## One-Time Setup

### GitHub Repo

Go to **Settings → Secrets and variables → Actions**:

| Name | Type | Value |
|---|---|---|
| `HF_TOKEN` | Secret | Hugging Face token with write access to the Space |
| `VITE_API_BASE_URL` | Variable | `https://beefstewbibi-avp-rag-system.hf.space` |

### Hugging Face Space

Go to your Space's **Settings**:

| Name | Type | Value |
|---|---|---|
| `ANTHROPIC_API_KEY` | Secret | Your Anthropic API key |
| `LLM_PROVIDER` | Variable | `anthropic` |
| `CORS_ORIGINS` | Variable | `https://huytran088.github.io` |

After setup, push any commit to `main` — both workflows trigger automatically.

---

## How the CI/CD Works

### Frontend → GitHub Pages (`deploy-gh-pages.yml`)

On every push to `main`:
1. Builds the React frontend with `VITE_BASE_PATH=/avp_rag_system/` and `VITE_API_BASE_URL` baked in
2. Deploys the static build to GitHub Pages via `actions/deploy-pages`

The `VITE_API_BASE_URL` variable is **build-time only** — Vite inlines it into the JS bundle. Changing it requires re-running the deploy workflow.

### Backend → HF Spaces (`sync-hf-spaces.yml`)

On every push to `main`:
1. Copies `hf-space/README.md` (which contains HF Spaces YAML front matter) to `README.md`
2. Force-pushes the entire repo to `huggingface.co/spaces/BeefStewBibi/avp-rag-system`
3. HF Spaces detects the push, builds `Dockerfile`, and restarts the container

The backend-only `Dockerfile` (not `Dockerfile.full`) is used — it skips the Node.js build stage and listens on port 7860 as required by HF Spaces.

### CI (`ci.yml`)

On every push/PR to `main`:
- Backend: `uv run pytest tests/`
- Frontend: `tsc --noEmit` + `vite build`

---

## Alternative: Local Backend + Tunnel

Use this if you want to run a local GPU model (Qwen3 via Ollama or vLLM) and expose it to the internet for the GitHub Pages frontend.

### Step 1: Set Up Local Backend

#### Option A: Ollama (Recommended)

Ollama manages model downloads and GPU inference with zero Docker config. It exposes an OpenAI-compatible API.

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model (RTX 4070 Super, 12 GB VRAM)
ollama pull qwen3:8b      # ~5 GB download, ~6 GB VRAM (quantized)

# Verify
ollama run qwen3:8b "write a hello world function"
```

Configure `.env`:
```
LLM_PROVIDER=vllm
VLLM_BASE_URL=http://localhost:11434/v1
VLLM_MODEL=qwen3:8b
VLLM_API_KEY=ollama
```

Start:
```bash
ollama serve &
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
```

#### Option B: vLLM via Docker Compose

Requires NVIDIA GPU with 16 GB+ VRAM and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

```bash
docker compose --profile vllm up --build -d
```

First run downloads ~16 GB of model weights (cached in `huggingface_cache` volume).

#### Qwen3 Model Sizes

| Model | Ollama tag | VRAM (quantized) | VRAM (full) |
|---|---|---|---|
| Qwen3-4B | `qwen3:4b` | ~4 GB | ~8 GB |
| Qwen3-8B | `qwen3:8b` | ~6 GB | ~16 GB |
| Qwen3-14B | `qwen3:14b` | ~10 GB | ~28 GB |

For RTX 4070 Super (12 GB), `qwen3:8b` via Ollama is the sweet spot.

### Step 2: Expose Backend to the Internet

Your local backend needs a public HTTPS URL so GitHub Pages can reach it.

#### Option A: ngrok (Quickest)

1. Install from [ngrok.com/download](https://ngrok.com/download)
2. `ngrok config add-authtoken <your-token>`
3. `ngrok http 8000`

This gives you a URL like `https://abc123.ngrok-free.app`. Free URLs change on restart; paid plans ($8/mo) give stable URLs.

#### Option B: Cloudflare Tunnel (Free, Stable)

```bash
# Install cloudflared and authenticate
cloudflared tunnel login

# Create and route
cloudflared tunnel create avp-rag
cloudflared tunnel route dns avp-rag api.yourdomain.com
cloudflared tunnel run --url http://localhost:8000 avp-rag
```

### Step 3: Configure CORS and Frontend

Set `CORS_ORIGINS` in `.env`:
```
CORS_ORIGINS=https://huytran088.github.io
```

Restart the backend after changing.

Update the GitHub repo variable `VITE_API_BASE_URL` to your tunnel URL, then re-run the deploy workflow:

**Actions → Deploy to GitHub Pages → Run workflow**

### Using Anthropic as Fallback

Configure Anthropic Claude as a fallback when your local Ollama/vLLM is unreachable:

```
LLM_PROVIDER=vllm
LLM_FALLBACK_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
VLLM_BASE_URL=http://localhost:11434/v1
VLLM_MODEL=qwen3:8b
```

The system tries the primary provider first and falls back to Anthropic on any error.

---

## Self-Hosted Docker (Full-Stack)

For teams who want a single-container deployment that serves both frontend and API:

```bash
cp .env.example .env
# Set ANTHROPIC_API_KEY or vLLM env vars in .env
docker compose up --build
```

Uses `Dockerfile.full`, which builds the React frontend in a Node stage and copies the built assets to `static/` in the Python container. Served at `http://localhost:8000`.

The `data/` directory is volume-mounted so you can add `.avp` files and re-ingest without rebuilding the image.

---

## Production Checklist

- [ ] HTTPS on the backend (HF Spaces / ngrok / Cloudflare provide this automatically)
- [ ] `CORS_ORIGINS` set to your exact frontend origin (e.g., `https://huytran088.github.io`)
- [ ] `.env` file is **not** committed to git — verify with `git status`
- [ ] `VITE_API_BASE_URL` set as a GitHub repo **variable** (not secret — it's embedded in the built JS)
- [ ] Backend health check passes before directing users to the frontend
- [ ] Rate limits in `api/dependencies.py` tuned for expected traffic (defaults: 10 generate/min, 30 retrieve/min)

---

## Troubleshooting

**Frontend renders blank page on GitHub Pages:**
- `BrowserRouter` must use `basename={import.meta.env.BASE_URL}` to match the `/avp_rag_system/` subpath
- Verify `VITE_BASE_PATH=/avp_rag_system/` was set at build time in the deploy workflow

**Frontend loads but API calls fail:**
- Open browser DevTools → Network tab, confirm requests go to the right URL
- Check CORS: the backend's `CORS_ORIGINS` must include your exact frontend origin
- `VITE_API_BASE_URL` is build-time only — changing the GitHub variable requires re-running the deploy workflow

**HF Space build fails:**
- Check `hf-space/README.md` has correct YAML front matter (`sdk: docker`, `app_port: 7860`)
- Verify `HF_TOKEN` secret in GitHub repo has write access to the Space
- Check Space build logs on huggingface.co

**503 "provider is not configured":**
- `LLM_PROVIDER=anthropic` requires `ANTHROPIC_API_KEY` in HF Space secrets
- `LLM_PROVIDER=vllm` requires `VLLM_BASE_URL` to point to a running server

**Ollama: "model not found":**
- Run `ollama list` to see installed models
- Model names are case-sensitive: `qwen3:8b`, not `Qwen3:8b`

**Ollama: out of memory:**
- Try `ollama pull qwen3:4b` (~4 GB VRAM)
- Check current usage: `nvidia-smi`

**vLLM container keeps restarting:**
- Check logs: `docker compose logs vllm`
- Try `Qwen/Qwen3-4B` or reduce `--max-model-len` in `docker-compose.yml`
- Verify NVIDIA Container Toolkit: `nvidia-smi` on the host

**ngrok URL changed:**
- Update `VITE_API_BASE_URL` in GitHub repo variables
- Re-run the deploy workflow (Actions → Deploy to GitHub Pages → Run workflow)
- Update `CORS_ORIGINS` in `.env` and restart the backend
