"""LLM provider abstraction with optional fallback."""

import os
import sys
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


# .__name__ references make Pyright see these as accessed; getattr re-resolves at
# call time so unittest.mock.patch can still override them.
_PROVIDER_FN_NAMES = {
    "anthropic": _call_anthropic.__name__,
    "vllm": _call_vllm.__name__,
}
_CONFIG_ENV_VAR = {"anthropic": "ANTHROPIC_API_KEY", "vllm": "VLLM_BASE_URL"}


def _get_provider_fn(name: str) -> Callable[[str], str]:
    # Look up by attribute so unittest.mock.patch on the module can override.
    return getattr(sys.modules[__name__], _PROVIDER_FN_NAMES[name])


def get_provider_name() -> str:
    return os.environ.get("LLM_PROVIDER", "anthropic")


def is_provider_configured() -> bool:
    env_var = _CONFIG_ENV_VAR.get(get_provider_name())
    return bool(env_var and os.environ.get(env_var))


def call_llm(prompt: str) -> str:
    provider = get_provider_name()
    fallback = os.environ.get("LLM_FALLBACK_PROVIDER", "")

    try:
        return _get_provider_fn(provider)(prompt)
    except Exception:
        if fallback in _PROVIDER_FN_NAMES:
            return _get_provider_fn(fallback)(prompt)
        raise
