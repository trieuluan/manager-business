"""AI provider router with external-first fallback."""

from __future__ import annotations

import frappe

from vn_localization.ai.providers.errors import ProviderError
from vn_localization.ai.providers.ollama import OllamaProvider
from vn_localization.ai.providers.openai_compatible import OpenAICompatibleProvider
from vn_localization.ai.settings import get_ai_settings, get_provider_order


def chat(messages, options=None):
	errors = []
	for provider in _get_ordered_providers():
		if not provider.is_available():
			continue

		try:
			response = provider.chat(messages, options=options)
			_log_provider(provider.name)
			return response
		except ProviderError as exc:
			errors.append(f"{provider.name}: {exc}")
			_log_provider_error(provider.name, exc)
			if not exc.retryable:
				continue

	raise ProviderError("All AI providers failed: " + " | ".join(errors), retryable=False)


def stream_chat(messages, options=None):
	errors = []
	for provider in _get_ordered_providers():
		if not provider.is_available():
			continue

		yielded_token = False
		try:
			for chunk in provider.stream_chat(messages, options=options):
				if chunk.get("type") == "token":
					yielded_token = True
				yield chunk
			_log_provider(provider.name)
			return
		except ProviderError as exc:
			_log_provider_error(provider.name, exc)
			if yielded_token:
				raise
			errors.append(f"{provider.name}: {exc}")
			continue

	raise ProviderError("All AI providers failed before streaming: " + " | ".join(errors), retryable=False)


def _get_ordered_providers():
	providers = _provider_map()
	ordered = []
	for name in get_provider_order():
		provider = providers.get(name)
		if provider:
			ordered.append(provider)
	if "ollama" not in [provider.name for provider in ordered]:
		ordered.append(providers["ollama"])
	return ordered


def _provider_map():
	settings = get_ai_settings()
	return {
		"openrouter": OpenAICompatibleProvider(
			name="openrouter",
			base_url=settings["openrouter_base_url"],
			api_key=settings["openrouter_api_key"],
			model=settings["openrouter_model"],
			timeout=settings["external_ai_timeout"],
			extra_headers=_openrouter_headers(settings),
		),
		"groq": OpenAICompatibleProvider(
			name="groq",
			base_url=settings["groq_base_url"],
			api_key=settings["groq_api_key"],
			model=settings["groq_model"],
			timeout=settings["external_ai_timeout"],
		),
		"openai": OpenAICompatibleProvider(
			name="openai",
			base_url=settings["openai_base_url"],
			api_key=settings["openai_api_key"],
			model=settings["openai_model"],
			timeout=settings["external_ai_timeout"],
		),
		"ollama": OllamaProvider(),
	}


def _openrouter_headers(settings):
	headers = {}
	if settings["openrouter_site_url"]:
		headers["HTTP-Referer"] = settings["openrouter_site_url"]
	if settings["openrouter_app_name"]:
		headers["X-Title"] = settings["openrouter_app_name"]
	return headers


def _log_provider(provider_name):
	frappe.logger("vn_localization").info(f"AI provider used: {provider_name}")


def _log_provider_error(provider_name, exc):
	frappe.logger("vn_localization").warning(f"AI provider failed: {provider_name}: {exc}")
