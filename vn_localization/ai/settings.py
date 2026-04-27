"""Configuration helpers for the local AI assistant."""

from __future__ import annotations

import frappe


DEFAULT_OLLAMA_BASE_URL = "http://ollama:11434"
DEFAULT_OLLAMA_MODEL = "qwen2.5:3b"
DEFAULT_OLLAMA_TIMEOUT = 60
DEFAULT_OLLAMA_NUM_PREDICT = 400
DEFAULT_OLLAMA_TEMPERATURE = 0.2


def get_ai_settings():
	return {
		"ollama_base_url": frappe.conf.get("ollama_base_url") or DEFAULT_OLLAMA_BASE_URL,
		"ollama_model": frappe.conf.get("ollama_model") or DEFAULT_OLLAMA_MODEL,
		"ollama_timeout": _get_int("ollama_timeout", DEFAULT_OLLAMA_TIMEOUT),
		"ollama_num_predict": _get_int("ollama_num_predict", DEFAULT_OLLAMA_NUM_PREDICT),
		"ollama_temperature": _get_float("ollama_temperature", DEFAULT_OLLAMA_TEMPERATURE),
	}


def get_ollama_options():
	settings = get_ai_settings()
	return {
		"temperature": settings["ollama_temperature"],
		"num_predict": settings["ollama_num_predict"],
	}


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
