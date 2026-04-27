"""Whitelisted AI chat endpoint for ERPNext Desk."""

from __future__ import annotations

import json

import frappe
from werkzeug.wrappers import Response

from vn_localization.ai.context import get_current_document_context
from vn_localization.ai.data_context import get_data_context
from vn_localization.ai.docs import get_relevant_context
from vn_localization.ai.menu_context import get_menu_context
from vn_localization.ai.providers.errors import ProviderError
from vn_localization.ai.providers.router import chat as provider_chat
from vn_localization.ai.providers.router import stream_chat as provider_stream_chat
from vn_localization.ai.settings import get_ollama_options, get_ai_settings
from vn_localization.ai.translation_context import get_translation_context


SYSTEM_PROMPT = """
Trợ lý ERPNext tiếng Việt. Trả lời ngắn, đúng trọng tâm, tối đa 5 bước/câu.
Không bịa số liệu. Dùng thuật ngữ tiếng Việt được cung cấp. Chỉ menu bên trái khi hỏi "ở đâu".
""".strip()


@frappe.whitelist()
def send_message(message, history=None, route=None, doctype=None, docname=None):
	_require_login()
	message = _clean_message(message)
	docs_context = get_relevant_context(message)
	erp_context = get_current_document_context(doctype=doctype, docname=docname, route=route)
	menu_context = get_menu_context(message)
	translation_context = get_translation_context(message, menu_context)
	data_context = get_data_context(message)
	messages = _build_messages(
		message,
		docs_context,
		erp_context,
		menu_context,
		translation_context,
		data_context,
		history,
	)

	try:
		response = provider_chat(messages)
	except ProviderError as exc:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI chat failed")
		frappe.throw(str(exc), title="AI Assistant")

	return {
		"message": _sanitize_response_text(response["content"]),
		"model": response["model"],
	}


@frappe.whitelist(methods=["POST"])
def stream_message(message, history=None, route=None, doctype=None, docname=None):
	_require_login()
	message = _clean_message(message)
	docs_context = get_relevant_context(message)
	erp_context = get_current_document_context(doctype=doctype, docname=docname, route=route)
	menu_context = get_menu_context(message)
	translation_context = get_translation_context(message, menu_context)
	data_context = get_data_context(message)
	messages = _build_messages(
		message,
		docs_context,
		erp_context,
		menu_context,
		translation_context,
		data_context,
		history,
	)

	return Response(
		_stream_events(messages),
		mimetype="text/event-stream",
		headers={
			"Cache-Control": "no-cache, no-transform",
			"X-Accel-Buffering": "no",
		},
	)


def _require_login():
	if frappe.session.user == "Guest":
		frappe.throw("Bạn cần đăng nhập để sử dụng trợ lý AI.", frappe.PermissionError)


def _clean_message(message):
	message = (message or "").strip()
	if not message:
		frappe.throw("Vui lòng nhập câu hỏi.")
	if len(message) > 2000:
		frappe.throw("Câu hỏi quá dài. Vui lòng rút gọn dưới 2000 ký tự.")
	return message


def _build_messages(
	message,
	docs_context,
	erp_context=None,
	menu_context=None,
	translation_context=None,
	data_context=None,
	history=None,
):
	messages = [{"role": "system", "content": SYSTEM_PROMPT}]

	context_blocks = []
	if docs_context:
		context_blocks.append(f"[Tài liệu]\n{docs_context}")
	if erp_context:
		context_blocks.append(f"[Chứng từ hiện tại]\n{erp_context}")
	if menu_context:
		context_blocks.append(f"[Menu]\n{menu_context}")
	if translation_context:
		context_blocks.append(f"[Thuật ngữ]\n{translation_context}")
	if data_context:
		context_blocks.append(f"[Dữ liệu kho]\n{data_context}")

	if context_blocks:
		messages.append({"role": "system", "content": "\n\n".join(context_blocks)})

	for item in _safe_history(history):
		messages.append(item)

	messages.append({"role": "user", "content": message})
	return messages


def _stream_events(messages):
	yield _sse("ready", {})
	yield (": " + (" " * 2048) + "\n\n").encode("utf-8")

	try:
		for chunk in provider_stream_chat(messages):
			if chunk["type"] == "token":
				yield _sse("token", {"content": chunk["content"], "model": chunk["model"]})
			elif chunk["type"] == "done":
				yield _sse("done", {"model": chunk["model"]})
				yield b": done\n\n"
	except ProviderError as exc:
		yield _sse("error", {"message": str(exc)})
	except Exception:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI stream failed")
		yield _sse("error", {"message": "AI stream failed unexpectedly."})


def _sse(event, data):
	return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n".encode("utf-8")


def _sanitize_response_text(text):
	replacements = {
		"Workspace Sidebar": "menu bên trái",
		"Purchase Receipt": "Phiếu nhập kho",
		"Sales Invoice": "Hóa đơn bán hàng",
		"Purchase Invoice": "Hóa đơn mua hàng",
		"Stock Entry": "Phiếu nhập xuất kho",
		"Stock Reconciliation": "Kiểm kê kho",
		"Journal Entry": "Bút toán",
		"Payment Entry": "Phiếu thu chi",
		"Delivery Note": "Phiếu giao hàng",
		"Sales Order": "Đơn bán hàng",
		"Purchase Order": "Đơn đặt hàng",
	}
	text = text or ""
	for source, target in replacements.items():
		text = text.replace(source, target)
	return text


def _safe_history(history):
	if not history:
		return []

	if isinstance(history, str):
		history = frappe.parse_json(history)

	safe_items = []
	for item in history[-4:]:
		role = item.get("role")
		content = (item.get("content") or "").strip()
		if role not in {"user", "assistant"} or not content:
			continue
		safe_items.append({"role": role, "content": content[:600]})
	return safe_items
