"""LLM provider abstraction with optional fallback."""

import os
from typing import Callable

import anthropic
import openai


def _call_anthropic(prompt: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Set the environment variable to enable generation."
        )
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def _call_vllm(prompt: str) -> str:
    base_url = os.environ.get("VLLM_BASE_URL", "http://vllm:8080/v1")
    model = os.environ.get("VLLM_MODEL", "Qwen/Qwen3-8B")
    api_key = os.environ.get("VLLM_API_KEY", "token-placeholder")
    client = openai.OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _get_provider_fn(name: str) -> Callable[[str], str]:
    providers: dict[str, Callable[[str], str]] = {
        "anthropic": _call_anthropic,
        "vllm": _call_vllm,
    }
    return providers[name]


def get_provider_name() -> str:
    return os.environ.get("LLM_PROVIDER", "anthropic")


def is_provider_configured() -> bool:
    provider = get_provider_name()
    if provider == "anthropic":
        return bool(os.environ.get("ANTHROPIC_API_KEY"))
    elif provider == "vllm":
        return bool(os.environ.get("VLLM_BASE_URL"))
    return False


def call_llm(prompt: str) -> str:
    provider = get_provider_name()
    fallback = os.environ.get("LLM_FALLBACK_PROVIDER", "")

    try:
        return _get_provider_fn(provider)(prompt)
    except Exception:
        if fallback and fallback in ("anthropic", "vllm"):
            return _get_provider_fn(fallback)(prompt)
        raise
