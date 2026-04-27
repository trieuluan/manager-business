"""Small Ollama HTTP client used by the ERPNext assistant."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import frappe


DEFAULT_MODEL = "qwen2.5:1.5b"
DEFAULT_BASE_URL = "http://ollama:11434"
DEFAULT_TIMEOUT = 60


class OllamaError(Exception):
	"""Raised when the local Ollama service cannot complete a request."""


def get_ollama_settings():
	return {
		"base_url": frappe.conf.get("ollama_base_url") or DEFAULT_BASE_URL,
		"model": frappe.conf.get("ollama_model") or DEFAULT_MODEL,
		"timeout": int(frappe.conf.get("ollama_timeout") or DEFAULT_TIMEOUT),
	}


def chat(messages, model=None, options=None):
	settings = get_ollama_settings()
	payload = {
		"model": model or settings["model"],
		"messages": messages,
		"stream": False,
	}
	if options:
		payload["options"] = options

	body = json.dumps(payload).encode("utf-8")
	request = Request(
		f"{settings['base_url'].rstrip('/')}/api/chat",
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
		raise OllamaError("Cannot connect to the local Ollama service") from exc
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
		"model": data.get("model") or payload["model"],
		"done": data.get("done"),
	}

