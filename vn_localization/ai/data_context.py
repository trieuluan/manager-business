"""Router for safe ERPNext data context tools."""

from __future__ import annotations

import frappe

from vn_localization.ai.tools.stock import get_stock_context


def get_data_context(question):
	context_parts = []

	try:
		stock_context = get_stock_context(question)
		if stock_context:
			context_parts.append(stock_context)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI stock context failed")

	return "\n\n".join(context_parts)

