"""ERPNext context builders for the local AI assistant."""

from __future__ import annotations

import frappe


MAX_CONTEXT_CHARS = 5000
MAX_CHILD_ROWS = 5

SAFE_FIELDNAMES = {
	"name",
	"owner",
	"creation",
	"modified",
	"docstatus",
	"status",
	"workflow_state",
	"title",
	"naming_series",
	"company",
	"currency",
	"customer",
	"customer_name",
	"supplier",
	"supplier_name",
	"party_type",
	"party",
	"party_name",
	"posting_date",
	"transaction_date",
	"schedule_date",
	"due_date",
	"delivery_date",
	"grand_total",
	"rounded_total",
	"base_grand_total",
	"outstanding_amount",
	"paid_amount",
	"total",
	"net_total",
	"total_qty",
	"territory",
	"warehouse",
	"set_warehouse",
	"item_code",
	"item_name",
	"item_group",
	"stock_uom",
	"qty",
	"actual_qty",
	"projected_qty",
	"valuation_rate",
	"is_stock_item",
	"disabled",
}

SAFE_CHILD_FIELDS = {
	"item_code",
	"item_name",
	"description",
	"qty",
	"uom",
	"rate",
	"amount",
	"warehouse",
	"account_head",
	"charge_type",
	"tax_amount",
	"total",
	"reference_doctype",
	"reference_name",
	"allocated_amount",
	"outstanding_amount",
}

CHILD_TABLES_TO_SUMMARIZE = {"items", "taxes", "references"}


def get_current_document_context(doctype=None, docname=None, route=None):
	doctype = _clean_value(doctype)
	docname = _clean_value(docname)
	route_text = _format_route(route)

	if not doctype or not docname:
		if route_text:
			return f"Ngữ cảnh màn hình hiện tại:\n- Route: {route_text}"
		return ""

	try:
		doc = frappe.get_doc(doctype, docname)
		doc.check_permission("read")
	except frappe.PermissionError:
		return (
			"Ngữ cảnh chứng từ hiện tại:\n"
			f"- Doctype: {doctype}\n"
			f"- Tên: {docname}\n"
			"- Người dùng hiện tại không có quyền đọc chi tiết chứng từ này."
		)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI document context failed")
		return ""

	lines = [
		"Ngữ cảnh chứng từ hiện tại:",
		f"- Doctype: {doc.doctype}",
		f"- Tên: {doc.name}",
	]
	if route_text:
		lines.append(f"- Route: {route_text}")

	lines.extend(_get_safe_field_lines(doc))
	lines.extend(_get_child_table_lines(doc))

	context = "\n".join(lines)
	return context[:MAX_CONTEXT_CHARS]


def _get_safe_field_lines(doc):
	lines = []
	for fieldname in sorted(SAFE_FIELDNAMES):
		if fieldname in {"name"}:
			continue
		value = doc.get(fieldname)
		if value in (None, "", []):
			continue
		lines.append(f"- {fieldname}: {_stringify(value)}")
	return lines


def _get_child_table_lines(doc):
	lines = []
	for table_field in CHILD_TABLES_TO_SUMMARIZE:
		rows = doc.get(table_field) or []
		if not rows:
			continue

		lines.append(f"- {table_field}: {len(rows)} dòng")
		for index, row in enumerate(rows[:MAX_CHILD_ROWS], start=1):
			row_parts = []
			for fieldname in SAFE_CHILD_FIELDS:
				value = row.get(fieldname)
				if value in (None, "", []):
					continue
				row_parts.append(f"{fieldname}={_stringify(value)}")
			if row_parts:
				lines.append(f"  {index}. " + "; ".join(row_parts[:8]))

		if len(rows) > MAX_CHILD_ROWS:
			lines.append(f"  ... còn {len(rows) - MAX_CHILD_ROWS} dòng khác")
	return lines


def _format_route(route):
	if isinstance(route, str):
		route = frappe.parse_json(route)
	if isinstance(route, list):
		return " / ".join(str(part) for part in route if part)
	return _clean_value(route)


def _clean_value(value):
	if value is None:
		return None
	value = str(value).strip()
	return value[:200] if value else None


def _stringify(value):
	if hasattr(value, "strftime"):
		return value.strftime("%Y-%m-%d")
	return str(value).replace("\n", " ")[:300]
