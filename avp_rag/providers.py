"""LLM provider abstraction with optional fallback."""

import os
import re
import sys
from typing import Callable

import anthropic
import openai


# Matches a leading Qwen-style reasoning block, so we can drop when thinkin is disabled
# but the served model still emits it. This is a bit hacky but allows us to use the same model for both providers.
_THINK_RE = re.compile(r"^\s*<think>\s*.*?</think>\s*", re.DOTALL)


def strip_thinking(text: str) -> str:
    """Strips leading Qwen-style reasoning blocks from the text."""
    if not text:
        return text
    return _THINK_RE.sub("", text, count=1)


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
    base_url = os.environ.get("VLLM_BASE_URL", "http://localhost:8001/v1")
    model = os.environ.get("VLLM_MODEL", "qwen3.6-27b-awq")
    api_key = os.environ.get("VLLM_API_KEY", "token-placeholder")

    # Qwen3.6 runs in thinking mode by default, so we strip out the leading reasoning block if present to avoid confusion
    # unless VLLM_THINKING_MODE is explicitly set to "enabled".
    enable_thinking = os.environ.get("VLLM_ENABLE_THINKING", "false").lower() == "true"

    client = openai.OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        max_tokens=int(os.environ.get("VLLM_MAX_TOKENS", "1024")),
        temperature=float(os.environ.get("VLLM_TEMPERATURE", "0.6")),
        top_p=float(os.environ.get("VLLM_TOP_P", "0.95")),
        messages=[{"role": "user", "content": prompt}],
        # top_k and the thinking switch are currently only supported in the vllm provider, so we set them here to avoid issues with the anthropic provider which doesn't support them.
        extra_body={
            "top_k": int(os.environ.get("VLLM_TOP_K", "20")),
            "chat_template_kwargs": {
                "enable_thinking": enable_thinking,
            },
        },
    )
    result = response.choices[0].message.content or ""
    if not enable_thinking:
        result = strip_thinking(result)
    return result


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
