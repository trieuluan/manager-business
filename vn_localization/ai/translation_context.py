"""Vietnamese translation context for AI answers."""

from __future__ import annotations

import csv
import json
from functools import lru_cache
from pathlib import Path

import frappe


APP_ROOT = Path(__file__).resolve().parents[1]
CSV_TRANSLATIONS = APP_ROOT / "translations" / "vi.csv"
PO_TRANSLATIONS = APP_ROOT / "locale" / "vi.po"
MAX_TRANSLATION_LINES = 18

ALWAYS_INCLUDE = {
	"Sales Invoice",
	"Purchase Invoice",
	"Purchase Receipt",
	"Stock Entry",
	"Stock Reconciliation",
	"Journal Entry",
	"Payment Entry",
	"Sales Order",
	"Purchase Order",
	"Delivery Note",
	"Quotation",
	"Customer",
	"Supplier",
	"Item",
	"Warehouse",
}


def get_translation_context(question, menu_context=None):
	translations = get_translations()
	keys = _find_relevant_keys(question, translations)

	for key in ALWAYS_INCLUDE:
		if key in translations:
			keys.add(key)

	for key in _extract_english_terms(menu_context):
		if key in translations:
			keys.add(key)

	if not keys:
		return ""

	lines = ["Thuật ngữ giao diện đã Việt hóa. Ưu tiên dùng tiếng Việt khi trả lời:"]
	for key in sorted(keys)[:MAX_TRANSLATION_LINES]:
		value = translations.get(key)
		if value and value != key:
			lines.append(f"- {key} = {value}")
	return "\n".join(lines)


@lru_cache(maxsize=1)
def get_translations():
	translations = {}
	translations.update(_read_csv_translations())
	translations.update(_read_po_translations())
	return translations


def _read_csv_translations():
	translations = {}
	try:
		with CSV_TRANSLATIONS.open(encoding="utf-8", newline="") as csvfile:
			for row in csv.reader(csvfile):
				if len(row) < 2:
					continue
				source = row[0].strip()
				target = row[1].strip()
				if source and target:
					translations[source] = target
	except Exception:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI CSV translation context failed")
	return translations


def _read_po_translations():
	translations = {}
	try:
		msgid = None
		msgstr = None
		active = None

		for line in PO_TRANSLATIONS.read_text(encoding="utf-8").splitlines():
			if line.startswith("msgid "):
				if msgid and msgstr:
					translations.setdefault(msgid, msgstr)
				msgid = _parse_po_string(line[6:])
				msgstr = ""
				active = "msgid"
				continue

			if line.startswith("msgstr "):
				msgstr = _parse_po_string(line[7:])
				active = "msgstr"
				continue

			if line.startswith('"') and active == "msgid":
				msgid = (msgid or "") + _parse_po_string(line)
				continue

			if line.startswith('"') and active == "msgstr":
				msgstr = (msgstr or "") + _parse_po_string(line)

		if msgid and msgstr:
			translations.setdefault(msgid, msgstr)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI PO translation context failed")
	return translations


def _parse_po_string(value):
	try:
		return json.loads(value)
	except Exception:
		return value.strip().strip('"')


def _find_relevant_keys(question, translations):
	query = _normalize(question)
	tokens = _tokens(query)
	keys = set()

	for source, target in translations.items():
		haystack = _normalize(f"{source} {target}")
		if any(token in haystack for token in tokens):
			keys.add(source)
		if len(keys) >= MAX_TRANSLATION_LINES:
			break

	return keys


def _extract_english_terms(text):
	if not text:
		return set()

	terms = set()
	for source in ALWAYS_INCLUDE:
		if source in text:
			terms.add(source)
	return terms


def _normalize(text):
	return str(text or "").casefold()


def _tokens(text):
	return [token.strip(".,:;!?()[]{}\"'") for token in text.split() if len(token.strip()) >= 3]
