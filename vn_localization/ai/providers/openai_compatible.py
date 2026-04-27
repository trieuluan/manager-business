"""OpenAI-compatible chat completions provider client."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from vn_localization.ai.providers.errors import ProviderError


class OpenAICompatibleProvider:
	def __init__(self, name, base_url, api_key, model, timeout=60, extra_headers=None):
		self.name = name
		self.base_url = base_url.rstrip("/")
		self.api_key = api_key
		self.model = model
		self.timeout = timeout
		self.extra_headers = extra_headers or {}

	def is_available(self):
		return bool(self.api_key and self.model)

	def chat(self, messages, options=None):
		data = self._request(messages, options=options, stream=False)
		choices = data.get("choices") or []
		message = (choices[0].get("message") if choices else {}) or {}
		content = message.get("content")
		if not content:
			raise ProviderError(f"{self.name} response did not include content")
		return {
			"content": content.strip(),
			"model": data.get("model") or self.model,
			"provider": self.name,
		}

	def stream_chat(self, messages, options=None):
		payload = self._payload(messages, options=options, stream=True)
		request = self._build_request(payload)

		try:
			with urlopen(request, timeout=self.timeout) as response:
				for raw_line in response:
					line = raw_line.decode("utf-8").strip()
					if not line or line.startswith(":"):
						continue
					if not line.startswith("data:"):
						continue

					data = line[5:].strip()
					if data == "[DONE]":
						yield {"type": "done", "model": self.model, "provider": self.name}
						return

					try:
						chunk = json.loads(data)
					except json.JSONDecodeError as exc:
						raise ProviderError(f"{self.name} returned an invalid stream chunk") from exc

					choices = chunk.get("choices") or []
					delta = (choices[0].get("delta") if choices else {}) or {}
					content = delta.get("content")
					if content:
						yield {
							"type": "token",
							"content": content,
							"model": chunk.get("model") or self.model,
							"provider": self.name,
						}

				yield {"type": "done", "model": self.model, "provider": self.name}
		except HTTPError as exc:
			raise self._http_error(exc) from exc
		except (URLError, TimeoutError) as exc:
			raise ProviderError(f"{self.name} connection failed: {exc}") from exc

	def _request(self, messages, options=None, stream=False):
		payload = self._payload(messages, options=options, stream=stream)
		request = self._build_request(payload)
		try:
			with urlopen(request, timeout=self.timeout) as response:
				return json.loads(response.read().decode("utf-8"))
		except HTTPError as exc:
			raise self._http_error(exc) from exc
		except (URLError, TimeoutError) as exc:
			raise ProviderError(f"{self.name} connection failed: {exc}") from exc
		except json.JSONDecodeError as exc:
			raise ProviderError(f"{self.name} returned invalid JSON") from exc

	def _payload(self, messages, options=None, stream=False):
		options = options or {}
		payload = {
			"model": self.model,
			"messages": messages,
			"stream": stream,
		}

		if "temperature" in options:
			payload["temperature"] = options["temperature"]
		if "num_predict" in options:
			payload["max_tokens"] = options["num_predict"]
		if "max_tokens" in options:
			payload["max_tokens"] = options["max_tokens"]

		return payload

	def _build_request(self, payload):
		headers = {
			"Authorization": f"Bearer {self.api_key}",
			"Content-Type": "application/json",
			"User-Agent": "Mozilla/5.0",
			**self.extra_headers,
		}
		return Request(
			f"{self.base_url}/chat/completions",
			data=json.dumps(payload).encode("utf-8"),
			headers=headers,
			method="POST",
		)

	def _http_error(self, exc):
		retryable = exc.code in {402, 408, 409, 429, 500, 502, 503, 504}
		detail = ""
		try:
			detail = exc.read().decode("utf-8")[:500]
		except Exception:
			pass
		message = f"{self.name} returned HTTP {exc.code}"
		if detail:
			message = f"{message}: {detail}"
		return ProviderError(message, retryable=retryable)

