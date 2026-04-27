"""Whitelisted AI chat endpoint for ERPNext Desk."""

from __future__ import annotations

import frappe

from vn_localization.ai.docs import get_relevant_context
from vn_localization.ai.ollama import OllamaError, chat as ollama_chat


SYSTEM_PROMPT = """
Bạn là trợ lý ERPNext cho người dùng Việt Nam.
Nhiệm vụ của bạn là hướng dẫn thao tác trong ERPNext ngắn gọn, rõ ràng, thực tế.
Chỉ trả lời dựa trên ngữ cảnh được cung cấp và kiến thức ERPNext phổ biến.
Nếu không chắc, hãy nói rõ rằng cần kiểm tra lại trên hệ thống.
Không bịa số liệu kinh doanh, khách hàng, hóa đơn, tồn kho hoặc dữ liệu nội bộ.
""".strip()


@frappe.whitelist()
def send_message(message, history=None):
	_require_login()
	message = _clean_message(message)
	context = get_relevant_context(message)
	messages = _build_messages(message, context, history)

	try:
		response = ollama_chat(
			messages,
			options={
				"temperature": 0.2,
				"num_predict": 700,
			},
		)
	except OllamaError as exc:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI chat failed")
		frappe.throw(str(exc), title="AI Assistant")

	return {
		"message": response["content"],
		"model": response["model"],
	}


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


def _build_messages(message, context, history=None):
	messages = [
		{"role": "system", "content": SYSTEM_PROMPT},
		{
			"role": "system",
			"content": f"Ngữ cảnh hướng dẫn nội bộ:\n{context or 'Chưa có tài liệu phù hợp.'}",
		},
	]

	for item in _safe_history(history):
		messages.append(item)

	messages.append({"role": "user", "content": message})
	return messages


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

