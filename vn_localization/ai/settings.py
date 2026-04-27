"""Configuration helpers for the local AI assistant."""

from __future__ import annotations

import json
import os

import frappe


DEFAULT_OLLAMA_BASE_URL = "http://ollama:11434"
DEFAULT_OLLAMA_MODEL = "qwen2.5:3b"
DEFAULT_OLLAMA_TIMEOUT = 120
DEFAULT_OLLAMA_NUM_PREDICT = 700
DEFAULT_OLLAMA_TEMPERATURE = 0.2
DEFAULT_PROVIDER_ORDER = ["openrouter", "groq", "openai", "ollama"]

DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_OPENROUTER_MODEL = "google/gemma-3-4b-it:free"
DEFAULT_GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"
DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_EXTERNAL_AI_TIMEOUT = 60


def get_ai_settings():
	return {
		"ollama_base_url": frappe.conf.get("ollama_base_url") or DEFAULT_OLLAMA_BASE_URL,
		"ollama_model": frappe.conf.get("ollama_model") or DEFAULT_OLLAMA_MODEL,
		"ollama_timeout": _get_int("ollama_timeout", DEFAULT_OLLAMA_TIMEOUT),
		"ollama_num_predict": _get_int("ollama_num_predict", DEFAULT_OLLAMA_NUM_PREDICT),
		"ollama_temperature": _get_float("ollama_temperature", DEFAULT_OLLAMA_TEMPERATURE),
		"ai_provider_order": get_provider_order(),
		"external_ai_timeout": _get_int("external_ai_timeout", DEFAULT_EXTERNAL_AI_TIMEOUT),
		"openrouter_base_url": frappe.conf.get("openrouter_base_url") or DEFAULT_OPENROUTER_BASE_URL,
		"openrouter_api_key": frappe.conf.get("openrouter_api_key") or os.environ.get("OPENROUTER_API_KEY"),
		"openrouter_model": frappe.conf.get("openrouter_model") or DEFAULT_OPENROUTER_MODEL,
		"openrouter_site_url": frappe.conf.get("openrouter_site_url"),
		"openrouter_app_name": frappe.conf.get("openrouter_app_name") or "vn_localization ERPNext Assistant",
		"groq_base_url": frappe.conf.get("groq_base_url") or DEFAULT_GROQ_BASE_URL,
		"groq_api_key": frappe.conf.get("groq_api_key") or os.environ.get("GROQ_API_KEY"),
		"groq_model": frappe.conf.get("groq_model") or DEFAULT_GROQ_MODEL,
		"openai_base_url": frappe.conf.get("openai_base_url") or DEFAULT_OPENAI_BASE_URL,
		"openai_api_key": frappe.conf.get("openai_api_key") or os.environ.get("OPENAI_API_KEY"),
		"openai_model": frappe.conf.get("openai_model") or DEFAULT_OPENAI_MODEL,
	}


def get_ollama_options():
	settings = get_ai_settings()
	return {
		"temperature": settings["ollama_temperature"],
		"num_predict": settings["ollama_num_predict"],
	}


def get_provider_order():
	value = frappe.conf.get("ai_provider_order")
	if not value:
		return DEFAULT_PROVIDER_ORDER
	if isinstance(value, list):
		return [str(provider).strip() for provider in value if str(provider).strip()]

	try:
		parsed = json.loads(value)
		if isinstance(parsed, list):
			return [str(provider).strip() for provider in parsed if str(provider).strip()]
	except (TypeError, ValueError):
		pass

	return [provider.strip() for provider in str(value).split(",") if provider.strip()]


def _get_int(key, default):
	try:
		return int(frappe.conf.get(key) or default)
	except (TypeError, ValueError):
		return default


def _get_float(key, default):
	try:
		return float(frappe.conf.get(key) or default)
	except (TypeError, ValueError):
		return default
