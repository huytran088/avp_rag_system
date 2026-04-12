"""Unit tests for providers.py"""

import os
import sys
from unittest.mock import patch, MagicMock

import pytest

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from providers import (
    _call_anthropic,
    _call_vllm,
    call_llm,
    is_provider_configured,
    get_provider_name,
)


class TestCallAnthropic:
    @patch("providers.anthropic.Anthropic")
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
    @patch("providers.openai.OpenAI")
    def test_returns_text(self, mock_cls):
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        mock_choice = MagicMock()
        mock_choice.message.content = "vllm output"
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        result = _call_vllm("hello")

        assert result == "vllm output"
        mock_cls.assert_called_once_with(
            base_url="http://vllm:8080/v1", api_key="token-placeholder"
        )


class TestCallLlm:
    @patch("providers._call_anthropic")
    def test_dispatches_to_anthropic(self, mock_anthropic):
        mock_anthropic.return_value = "anthropic result"
        with patch.dict(os.environ, {"LLM_PROVIDER": "anthropic"}):
            result = call_llm("prompt")
        assert result == "anthropic result"

    @patch("providers._call_vllm")
    def test_dispatches_to_vllm(self, mock_vllm):
        mock_vllm.return_value = "vllm result"
        with patch.dict(os.environ, {"LLM_PROVIDER": "vllm"}):
            result = call_llm("prompt")
        assert result == "vllm result"

    @patch("providers._call_vllm")
    @patch("providers._call_anthropic")
    def test_fallback_on_error(self, mock_anthropic, mock_vllm):
        mock_anthropic.side_effect = RuntimeError("no key")
        mock_vllm.return_value = "fallback result"
        with patch.dict(
            os.environ, {"LLM_PROVIDER": "anthropic", "LLM_FALLBACK_PROVIDER": "vllm"}
        ):
            result = call_llm("prompt")
        assert result == "fallback result"

    @patch("providers._call_anthropic")
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
