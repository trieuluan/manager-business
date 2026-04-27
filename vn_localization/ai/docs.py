"""Lightweight documentation retrieval for the local AI assistant."""

from __future__ import annotations

from pathlib import Path

import frappe


DOCS_DIR = Path(__file__).resolve().parent / "docs"
MAX_CONTEXT_CHARS = 6000


def get_relevant_context(question):
	question = (question or "").lower()
	docs = []

	for path in sorted(DOCS_DIR.glob("*.md")):
		content = path.read_text(encoding="utf-8")
		score = _score_doc(question, content)
		if score:
			docs.append((score, path.stem, content))

	if not docs:
		return _fallback_context()

	docs.sort(key=lambda item: item[0], reverse=True)
	context_parts = []
	total_chars = 0

	for _score, title, content in docs[:3]:
		block = f"# {title}\n{content.strip()}"
		if total_chars + len(block) > MAX_CONTEXT_CHARS:
			break
		context_parts.append(block)
		total_chars += len(block)

	return "\n\n---\n\n".join(context_parts)


def _score_doc(question, content):
	score = 0
	text = content.lower()
	for token in _tokens(question):
		if token in text:
			score += 1
	return score


def _tokens(text):
	return [token.strip(".,:;!?()[]{}\"'") for token in text.split() if len(token.strip()) >= 3]


def _fallback_context():
	try:
		return (DOCS_DIR / "general.md").read_text(encoding="utf-8")
	except FileNotFoundError:
		frappe.log_error("Missing AI assistant fallback docs", "vn_localization AI")
		return ""

