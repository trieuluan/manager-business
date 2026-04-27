"""Provider adapter for local Ollama."""

from __future__ import annotations

from vn_localization.ai import ollama
from vn_localization.ai.providers.errors import ProviderError


class OllamaProvider:
	name = "ollama"

	def is_available(self):
		return True

	def chat(self, messages, options=None):
		try:
			response = ollama.chat(messages, options=options)
		except ollama.OllamaError as exc:
			raise ProviderError(str(exc), retryable=False) from exc

		return {
			**response,
			"provider": self.name,
		}

	def stream_chat(self, messages, options=None):
		try:
			for chunk in ollama.stream_chat(messages, options=options):
				yield {
					**chunk,
					"provider": self.name,
				}
		except ollama.OllamaError as exc:
			raise ProviderError(str(exc), retryable=False) from exc

