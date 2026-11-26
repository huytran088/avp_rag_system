"""Unit tests for avp_rag/providers.py"""

import os
from unittest.mock import patch, MagicMock

import pytest

from avp_rag.providers import (
    _call_anthropic,
    _call_vllm,
    _call_hf,
    _call_gemini,
    DEFAULT_HF_MODEL,
    GEMINI_OPENAI_URL,
    HF_ROUTER_URL,
    call_llm,
    is_provider_configured,
    get_provider_name,
)


class TestCallAnthropic:
    @patch("avp_rag.providers.anthropic.Anthropic")
    def test_returns_text(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_msg = MagicMock()
        mock_msg.content = [MagicMock(text="generated output")]
        mock_client.messages.create.return_value = mock_msg

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            result = _call_anthropic("hello")

        assert result == "generated output"
        mock_client.messages.create.assert_called_once()

    def test_raises_without_key(self):
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("ANTHROPIC_API_KEY", None)
            with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
                _call_anthropic("hello")


class TestCallVllm:
    @patch("avp_rag.providers.openai.OpenAI")
    def test_returns_text(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_choice = MagicMock()
        mock_choice.message.content = "vllm output"
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        # A local .env (loaded by api.main in other tests) may set these; test the defaults
        env = {k: v for k, v in os.environ.items() if k not in ("VLLM_BASE_URL", "VLLM_API_KEY")}
        with patch.dict(os.environ, env, clear=True):
            result = _call_vllm("hello")

        assert result == "vllm output"
        mock_cls.assert_called_once_with(
            base_url="http://localhost:8001/v1", api_key="token-placeholder"
        )


class TestCallLlm:
    @patch("avp_rag.providers._call_anthropic")
    def test_dispatches_to_anthropic(self, mock_anthropic):
        mock_anthropic.return_value = "anthropic result"
        with patch.dict(os.environ, {"LLM_PROVIDER": "anthropic"}):
            result = call_llm("prompt")
        assert result == "anthropic result"

    @patch("avp_rag.providers._call_vllm")
    def test_dispatches_to_vllm(self, mock_vllm):
        mock_vllm.return_value = "vllm result"
        with patch.dict(os.environ, {"LLM_PROVIDER": "vllm"}):
            result = call_llm("prompt")
        assert result == "vllm result"

    @patch("avp_rag.providers._call_vllm")
    @patch("avp_rag.providers._call_anthropic")
    def test_fallback_on_error(self, mock_anthropic, mock_vllm):
        mock_anthropic.side_effect = RuntimeError("no key")
        mock_vllm.return_value = "fallback result"
        with patch.dict(
            os.environ, {"LLM_PROVIDER": "anthropic", "LLM_FALLBACK_PROVIDER": "vllm"}
        ):
            result = call_llm("prompt")
        assert result == "fallback result"

    @patch("avp_rag.providers._call_anthropic")
    def test_no_fallback_reraises(self, mock_anthropic):
        mock_anthropic.side_effect = RuntimeError("no key")
        with patch.dict(os.environ, {"LLM_PROVIDER": "anthropic", "LLM_FALLBACK_PROVIDER": ""}):
            with pytest.raises(RuntimeError, match="no key"):
                call_llm("prompt")


class TestIsProviderConfigured:
    def test_anthropic_configured(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "anthropic", "ANTHROPIC_API_KEY": "key"}):
            assert is_provider_configured() is True

    def test_anthropic_not_configured(self):
        env = {"LLM_PROVIDER": "anthropic"}
        with patch.dict(os.environ, env, clear=True):
            assert is_provider_configured() is False

    def test_vllm_configured(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "vllm", "VLLM_BASE_URL": "http://localhost:8080/v1"}):
            assert is_provider_configured() is True

    def test_vllm_not_configured(self):
        env = {"LLM_PROVIDER": "vllm"}
        with patch.dict(os.environ, env, clear=True):
            assert is_provider_configured() is False


class TestGetProviderName:
    def test_default(self):
        with patch.dict(os.environ, {}, clear=True):
            assert get_provider_name() == "anthropic"

    def test_explicit(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "vllm"}):
            assert get_provider_name() == "vllm"


def _mock_openai(mock_cls, content="hosted output"):
    mock_client = MagicMock()
    mock_cls.return_value = mock_client
    mock_choice = MagicMock()
    mock_choice.message.content = content
    mock_client.chat.completions.create.return_value = MagicMock(choices=[mock_choice])
    return mock_client


class TestCallHostedProviders:
    @patch("avp_rag.providers.openai.OpenAI")
    def test_hf_uses_router_and_default_model(self, mock_cls):
        client = _mock_openai(mock_cls)
        with patch.dict(os.environ, {"HF_TOKEN": "hf_x"}, clear=True):
            assert _call_hf("hello") == "hosted output"
        mock_cls.assert_called_once_with(base_url=HF_ROUTER_URL, api_key="hf_x")
        assert client.chat.completions.create.call_args.kwargs["model"] == DEFAULT_HF_MODEL

    @patch("avp_rag.providers.openai.OpenAI")
    def test_hf_model_override_and_think_stripped(self, mock_cls):
        client = _mock_openai(mock_cls, "<think>hmm</think>\nfun f():\nend fun")
        env = {"HF_TOKEN": "hf_x", "HF_MODEL": "zai-org/GLM-5.3-Flash"}
        with patch.dict(os.environ, env, clear=True):
            assert _call_hf("hello") == "fun f():\nend fun"
        assert client.chat.completions.create.call_args.kwargs["model"] == "zai-org/GLM-5.3-Flash"

    @patch("avp_rag.providers.openai.OpenAI")
    def test_gemini_uses_openai_compat_endpoint(self, mock_cls):
        _mock_openai(mock_cls)
        with patch.dict(os.environ, {"GEMINI_API_KEY": "g"}, clear=True):
            assert _call_gemini("hello") == "hosted output"
        mock_cls.assert_called_once_with(base_url=GEMINI_OPENAI_URL, api_key="g")

    @pytest.mark.parametrize("fn", [_call_hf, _call_gemini])
    def test_missing_key_raises(self, fn):
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(RuntimeError):
                fn("hello")

    @pytest.mark.parametrize(
        "provider,key", [("hf", "HF_TOKEN"), ("gemini", "GEMINI_API_KEY")]
    )
    def test_is_configured(self, provider, key):
        with patch.dict(os.environ, {"LLM_PROVIDER": provider}, clear=True):
            assert is_provider_configured() is False
        with patch.dict(os.environ, {"LLM_PROVIDER": provider, key: "k"}, clear=True):
            assert is_provider_configured() is True

    @patch("avp_rag.providers._call_gemini", return_value="from gemini")
    @patch("avp_rag.providers._call_hf", side_effect=RuntimeError("down"))
    def test_hf_falls_back_to_gemini(self, mock_hf, mock_gemini):
        env = {"LLM_PROVIDER": "hf", "LLM_FALLBACK_PROVIDER": "gemini"}
        with patch.dict(os.environ, env, clear=True):
            assert call_llm("p") == "from gemini"
