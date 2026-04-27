"""Whitelisted AI chat endpoint for ERPNext Desk."""

from __future__ import annotations

import json

import frappe
from werkzeug.wrappers import Response

from vn_localization.ai.context import get_current_document_context
from vn_localization.ai.docs import get_relevant_context
from vn_localization.ai.ollama import OllamaError, chat as ollama_chat
from vn_localization.ai.ollama import stream_chat as ollama_stream_chat
from vn_localization.ai.settings import get_ollama_options


SYSTEM_PROMPT = """
Bạn là trợ lý ERPNext cho người dùng Việt Nam.
Trả lời đúng trọng tâm câu hỏi, ưu tiên câu trả lời ngắn và có thể làm ngay.

Quy tắc bắt buộc:
- Không mở rộng sang chủ đề khác nếu người dùng không hỏi.
- Không giải thích lý thuyết dài dòng.
- Nếu là câu hỏi thao tác, trả lời tối đa 5 bước.
- Nếu là câu hỏi khái niệm, trả lời tối đa 5 câu.
- Nếu thiếu dữ liệu hoặc không chắc cấu hình hệ thống, nói rõ cần kiểm tra lại.
- Không bịa số liệu kinh doanh, khách hàng, hóa đơn, tồn kho hoặc dữ liệu nội bộ.
- Nếu câu trả lời có thể ngắn trong 1-2 câu, hãy trả lời ngắn như vậy.
""".strip()


@frappe.whitelist()
def send_message(message, history=None, route=None, doctype=None, docname=None):
	_require_login()
	message = _clean_message(message)
	docs_context = get_relevant_context(message)
	erp_context = get_current_document_context(doctype=doctype, docname=docname, route=route)
	messages = _build_messages(message, docs_context, erp_context, history)

	try:
		response = ollama_chat(
			messages,
			options=get_ollama_options(),
		)
	except OllamaError as exc:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI chat failed")
		frappe.throw(str(exc), title="AI Assistant")

	return {
		"message": response["content"],
		"model": response["model"],
	}


@frappe.whitelist(methods=["POST"])
def stream_message(message, history=None, route=None, doctype=None, docname=None):
	_require_login()
	message = _clean_message(message)
	docs_context = get_relevant_context(message)
	erp_context = get_current_document_context(doctype=doctype, docname=docname, route=route)
	messages = _build_messages(message, docs_context, erp_context, history)

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


def _build_messages(message, docs_context, erp_context=None, history=None):
	messages = [
		{"role": "system", "content": SYSTEM_PROMPT},
		{
			"role": "system",
			"content": f"Ngữ cảnh hướng dẫn nội bộ:\n{docs_context or 'Chưa có tài liệu phù hợp.'}",
		},
	]
	if erp_context:
		messages.append(
			{
				"role": "system",
				"content": (
					"Dữ liệu ERPNext hiện tại người dùng đang xem. "
					"Chỉ dùng dữ liệu này nếu nó liên quan trực tiếp tới câu hỏi; "
					"không suy diễn thêm ngoài dữ liệu được cung cấp.\n"
					f"{erp_context}"
				),
			}
		)

	for item in _safe_history(history):
		messages.append(item)

	messages.append({"role": "user", "content": message})
	return messages


def _stream_events(messages):
	yield _sse("ready", {})
	yield (": " + (" " * 2048) + "\n\n").encode("utf-8")

	try:
		for chunk in ollama_stream_chat(
			messages,
			options=get_ollama_options(),
		):
			if chunk["type"] == "token":
				yield _sse("token", {"content": chunk["content"], "model": chunk["model"]})
			elif chunk["type"] == "done":
				yield _sse("done", {"model": chunk["model"]})
				yield b": done\n\n"
	except OllamaError as exc:
		yield _sse("error", {"message": str(exc)})
	except Exception:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI stream failed")
		yield _sse("error", {"message": "AI stream failed unexpectedly."})


def _sse(event, data):
	return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n".encode("utf-8")


def _safe_history(history):
	if not history:
		return []

	if isinstance(history, str):
		history = frappe.parse_json(history)

	safe_items = []
	for item in history[-6:]:
		role = item.get("role")
		content = (item.get("content") or "").strip()
		if role not in {"user", "assistant"} or not content:
			continue
		safe_items.append({"role": role, "content": content[:1500]})
	return safe_items
