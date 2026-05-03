"""Qwen Cloud provider - fallback final when all external providers fail."""

from __future__ import annotations

from vn_localization.ai import ollama
from vn_localization.ai.providers.errors import ProviderError


class QwenCloudProvider:
    """Provider for Qwen Cloud models via Ollama API."""

    def __init__(self, base_url=None, model="qwen3.5:cloud", timeout=120):
        self.name = "qwen3.5:cloud"
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

    def is_available(self):
        return True

    def chat(self, messages, options=None):
        try:
            response = ollama.chat(
                messages,
                model=self.model,
                options=options,
                base_url=self.base_url,
            )
        except ollama.OllamaError as exc:
            raise ProviderError(str(exc), retryable=False) from exc

        return {
            **response,
            "provider": self.name,
        }

    def stream_chat(self, messages, options=None):
        try:
            for chunk in ollama.stream_chat(
                messages,
                model=self.model,
                options=options,
                base_url=self.base_url,
            ):
                yield {
                    **chunk,
                    "provider": self.name,
                }
        except ollama.OllamaError as exc:
            raise ProviderError(str(exc), retryable=False) from exc
