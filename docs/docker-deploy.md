# Deployment Guide

This guide covers deploying the AVP RAG system for long-term online use. The recommended setup is:

- **Frontend** on GitHub Pages (free static hosting, auto-deployed via CI/CD)
- **Backend** on your local machine or a GPU server
- **LLM** via Ollama (simplest) or vLLM (Docker)

## Architecture

```
GitHub Pages                          Your Machine (GPU)
huytran088.github.io/avp_rag_system   ┌─────────────────────┐
     |                                │ FastAPI (port 8000)  │
  Static React ── fetch /api/* ──────>│         |            │
     (Vite build)    via ngrok/tunnel │ Ollama  or  vLLM     │
                                      │ (Qwen3, GPU)         │
                                      └─────────────────────┘
```

---

## Step 1: Backend Setup (Local Machine)

### Option A: Ollama (Recommended for Local)

Ollama manages model downloads, caching, and GPU inference with zero Docker GPU config. It exposes an OpenAI-compatible API that our `providers.py` already speaks.

1. **Install Ollama:**

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Pull a Qwen3 model:**

   ```bash
   # For RTX 4070 Super (12 GB VRAM):
   ollama pull qwen3:8b      # ~5 GB download, fits in 12 GB VRAM
   # Smaller alternative:
   ollama pull qwen3:4b      # ~2.5 GB, faster responses
   ```

   Ollama quantizes models automatically — `qwen3:8b` uses Q4_K_M quantization by default, which fits comfortably in 12 GB VRAM unlike the full-precision 16 GB that vLLM would need.

3. **Verify it works:**

   ```bash
   ollama run qwen3:8b "Hello, write a hello world function"
   ```

4. **Configure the app:**

   Edit `.env`:
   ```
   LLM_PROVIDER=vllm
   VLLM_BASE_URL=http://localhost:11434/v1
   VLLM_MODEL=qwen3:8b
   VLLM_API_KEY=ollama
   ```

   Note: We reuse the `vllm` provider since Ollama exposes the same OpenAI-compatible API. The `VLLM_API_KEY` value doesn't matter — Ollama ignores it, but the OpenAI SDK requires a non-empty string.

5. **Start the backend:**

   ```bash
   # Ollama runs as a system service after install, or start manually:
   ollama serve &

   # Start the API server:
   uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```

6. **Test:**

   ```bash
   curl http://localhost:8000/api/health
   # {"status":"ok","retriever_loaded":true,"provider_configured":true}

   curl -X POST http://localhost:8000/api/generate \
     -H 'Content-Type: application/json' \
     -d '{"message": "write a function to add two numbers"}'
   ```

### Option B: vLLM (Docker, Full Precision)

Use this if you want full-precision inference or are deploying to a cloud GPU server with 16 GB+ VRAM.

1. **Requirements:**
   - NVIDIA GPU with 16 GB+ VRAM
   - Docker Engine 24+ with [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

2. **Configure `.env`:**
   ```
   LLM_PROVIDER=vllm
   VLLM_BASE_URL=http://vllm:8080/v1
   VLLM_MODEL=Qwen/Qwen3-8B
   ```

3. **Start with Docker Compose:**
   ```bash
   docker compose --profile vllm up --build -d
   ```

   First run downloads ~16 GB of model weights (cached in `huggingface_cache` volume).

### Qwen3 Model Sizes

| Model | Ollama tag | VRAM (quantized) | VRAM (full) | Quality |
|---|---|---|---|---|
| Qwen3-4B | `qwen3:4b` | ~4 GB | ~8 GB | Good for simple tasks |
| Qwen3-8B | `qwen3:8b` | ~6 GB | ~16 GB | Good general quality |
| Qwen3-14B | `qwen3:14b` | ~10 GB | ~28 GB | Best quality |

For your RTX 4070 Super (12 GB), `qwen3:8b` via Ollama is the sweet spot.

---

## Step 2: Expose Backend to the Internet

Your local machine doesn't have a public IP, so you need a tunnel for GitHub Pages to reach your API.

### Option A: ngrok (Quickest)

1. **Install:** [ngrok.com/download](https://ngrok.com/download)
2. **Sign up** for a free account and run `ngrok config add-authtoken <your-token>`
3. **Start the tunnel:**

   ```bash
   ngrok http 8000
   ```

   This gives you a URL like `https://abc123.ngrok-free.app`. This is your `VITE_API_BASE_URL`.

   Note: Free ngrok URLs change on restart. For a stable URL, use a paid plan ($8/mo) or Cloudflare Tunnel.

### Option B: Cloudflare Tunnel (Free, Stable URL)

1. **Install cloudflared:** [developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
2. **Authenticate:** `cloudflared tunnel login`
3. **Create a tunnel:**
   ```bash
   cloudflared tunnel create avp-rag
   cloudflared tunnel route dns avp-rag api.yourdomain.com
   ```
4. **Run it:**
   ```bash
   cloudflared tunnel run --url http://localhost:8000 avp-rag
   ```

   This gives a stable subdomain that persists across restarts.

### Configure CORS

Set `CORS_ORIGINS` in `.env` to allow your GitHub Pages domain:

```
CORS_ORIGINS=https://huytran088.github.io
```

If using ngrok, also add the ngrok URL:
```
CORS_ORIGINS=https://huytran088.github.io,https://abc123.ngrok-free.app
```

---

## Step 3: Deploy Frontend to GitHub Pages

The frontend is automatically built and deployed by the CI/CD workflow on every push to `main`.

### One-Time Setup

1. **Go to your repo Settings > Pages**
2. **Source**: Select "GitHub Actions" (not "Deploy from a branch")
3. **Add the repository variable** for your backend URL:
   - Go to Settings > Secrets and variables > Actions > Variables
   - Add `VITE_API_BASE_URL` = your backend URL (e.g., `https://abc123.ngrok-free.app` or `https://api.yourdomain.com`)

### How It Works

On every push to `main`:

1. **CI workflow** (`.github/workflows/ci.yml`) runs:
   - Backend unit tests (`uv run pytest tests/`)
   - Frontend type check and build

2. **Deploy workflow** (`.github/workflows/deploy-gh-pages.yml`) runs:
   - Builds the frontend with `VITE_API_BASE_URL` and `VITE_BASE_PATH=/avp_rag_system/` baked in
   - Deploys to GitHub Pages via the official `actions/deploy-pages` action

3. Frontend is live at `https://huytran088.github.io/avp_rag_system/`

### Manual Deploy (Without CI)

```bash
cd frontend
VITE_BASE_PATH=/avp_rag_system/ VITE_API_BASE_URL=https://your-backend-url npm run deploy:gh-pages
```

### Updating the Backend URL

If your tunnel URL changes (e.g., ngrok restart on free plan):

1. Go to repo Settings > Secrets and variables > Actions > Variables
2. Update `VITE_API_BASE_URL` to the new URL
3. Re-run the deploy workflow (Actions tab > Deploy to GitHub Pages > Run workflow)

Also update `CORS_ORIGINS` in your local `.env` to include the new URL.

---

## Using Anthropic as Fallback

You can configure Anthropic Claude as a fallback when Ollama/vLLM is unreachable (e.g., your machine is off):

```
LLM_PROVIDER=vllm
LLM_FALLBACK_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

VLLM_BASE_URL=http://localhost:11434/v1
VLLM_MODEL=qwen3:8b
```

The system tries vLLM/Ollama first and falls back to Anthropic on any error.

---

## Production Checklist

- [ ] HTTPS on the backend (ngrok/Cloudflare provide this automatically)
- [ ] `CORS_ORIGINS` set to your actual GitHub Pages URL
- [ ] `.env` file is **not** committed to git (check `.gitignore`)
- [ ] `VITE_API_BASE_URL` set as a GitHub repo variable (not a secret — it's embedded in the built JS)
- [ ] Ollama/vLLM is running and responsive before directing users to the frontend
- [ ] Rate limits in `api/dependencies.py` tuned for expected traffic (defaults: 10 generate/min, 30 retrieve/min)

## Troubleshooting

**Frontend loads but API calls fail:**
- Open browser DevTools > Network tab, check if `/api/generate` requests are going to the right URL
- Check CORS: the backend must have your GitHub Pages origin in `CORS_ORIGINS`
- Check `VITE_API_BASE_URL` was set at **build time** (Vite inlines it during build, it's not read at runtime)

**Ollama: "model not found":**
- Run `ollama list` to see installed models
- Model names are case-sensitive: `qwen3:8b`, not `Qwen3:8b`

**Ollama: out of memory:**
- Try a smaller model: `ollama pull qwen3:4b`
- Close other GPU-using apps (games, other ML models)
- Check usage: `nvidia-smi`

**503 "provider is not configured":**
- `LLM_PROVIDER=vllm` requires `VLLM_BASE_URL` to be set
- `LLM_PROVIDER=anthropic` requires `ANTHROPIC_API_KEY` to be set

**vLLM container keeps restarting:**
- Check logs: `docker compose logs vllm`
- Out of GPU memory — try `Qwen/Qwen3-4B` or reduce `--max-model-len`
- NVIDIA driver/toolkit not installed — run `nvidia-smi` on the host

**ngrok URL changed:**
- Update `VITE_API_BASE_URL` in GitHub repo variables and re-run the deploy workflow
- Update `CORS_ORIGINS` in `.env` and restart the backend
