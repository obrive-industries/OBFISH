from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.config import Config
from app.utils.llm_client import LLMClient, LLMTarget


class ProviderRateLimitError(RuntimeError):
    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message)
        self.status_code = 429


def _mock_response(content):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


def test_cross_provider_automatic_failover():
    client = object.__new__(LLMClient)
    client._key_index = 0

    groq_client = MagicMock()
    groq_client.chat.completions.create.side_effect = ProviderRateLimitError("Groq 429 TPD limit")

    mistral_client = MagicMock()
    mistral_client.chat.completions.create.return_value = _mock_response("Response from Mistral AI 1B pool")

    client.targets = [
        LLMTarget(client=groq_client, model="llama-3.3-70b-versatile", base_url="https://api.groq.com/openai/v1", name="Groq-Primary"),
        LLMTarget(client=mistral_client, model="open-mistral-nemo", base_url="https://api.mistral.ai/v1", name="Mistral-Boost"),
    ]

    result = client.chat(messages=[{"role": "user", "content": "Hello"}])
    assert result == "Response from Mistral AI 1B pool"
    assert groq_client.chat.completions.create.called
    assert mistral_client.chat.completions.create.called
