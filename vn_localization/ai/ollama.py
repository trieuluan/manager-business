"""Small Ollama HTTP client used by the ERPNext assistant."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from vn_localization.ai.settings import get_ai_settings


class OllamaError(Exception):
	"""Raised when the Ollama service (local or cloud) cannot complete a request."""


def get_ollama_settings(model=None):
	settings = get_ai_settings()
	return {
		"base_url": settings["ollama_base_url"],
		"model": model or settings["ollama_model"],
		"timeout": settings["ollama_timeout"],
	}


def chat(messages, model=None, options=None, base_url=None):
	settings = get_ollama_settings(model)
	base_url = base_url or settings["base_url"]
	payload = {
		"model": settings["model"],
		"messages": messages,
		"stream": False,
	}
	if options:
		payload["options"] = options

	body = json.dumps(payload).encode("utf-8")
	request = Request(
		f"{base_url.rstrip('/')}/api/chat",
		data=body,
		headers={"Content-Type": "application/json"},
		method="POST",
	)

	try:
		with urlopen(request, timeout=settings["timeout"]) as response:
			data = json.loads(response.read().decode("utf-8"))
	except HTTPError as exc:
		raise OllamaError(f"Ollama returned HTTP {exc.code}") from exc
	except URLError as exc:
		raise OllamaError("Cannot connect to Ollama service") from exc
	except TimeoutError as exc:
		raise OllamaError("Ollama request timed out") from exc
	except json.JSONDecodeError as exc:
		raise OllamaError("Ollama returned an invalid response") from exc

	message = data.get("message") or {}
	content = message.get("content")
	if not content:
		raise OllamaError("Ollama response did not include a message")

	return {
		"content": content.strip(),
		"model": data.get("model") or settings["model"],
		"done": data.get("done"),
	}


def stream_chat(messages, model=None, options=None, base_url=None):
	settings = get_ollama_settings(model)
	base_url = base_url or settings["base_url"]
	payload = {
		"model": settings["model"],
		"messages": messages,
		"stream": True,
	}
	if options:
		payload["options"] = options

	body = json.dumps(payload).encode("utf-8")
	request = Request(
		f"{base_url.rstrip('/')}/api/chat",
		data=body,
		headers={"Content-Type": "application/json"},
		method="POST",
	)

	try:
		with urlopen(request, timeout=settings["timeout"]) as response:
			for line in response:
				if not line:
					continue
				try:
					data = json.loads(line.decode("utf-8"))
				except json.JSONDecodeError as exc:
					raise OllamaError("Ollama returned an invalid stream chunk") from exc

				message = data.get("message") or {}
				content = message.get("content")
				if content:
					yield {
						"type": "token",
						"content": content,
						"model": data.get("model") or settings["model"],
					}
				if data.get("done"):
					yield {
						"type": "done",
						"model": data.get("model") or settings["model"],
					}
					return
	except HTTPError as exc:
		raise OllamaError(f"Ollama returned HTTP {exc.code}") from exc
	except URLError as exc:
		raise OllamaError("Cannot connect to Ollama service") from exc
	except TimeoutError as exc:
		raise OllamaError("Ollama request timed out") from exc
