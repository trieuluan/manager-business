"""Stock and item data helpers for AI context."""

from __future__ import annotations

import re

import frappe


MAX_ITEMS = 3
MAX_BINS_PER_ITEM = 8

STOCK_KEYWORDS = {
	"tồn kho",
	"ton kho",
	"còn hàng",
	"con hang",
	"còn bao nhiêu",
	"con bao nhieu",
	"số lượng tồn",
	"so luong ton",
	"kho",
	"mã hàng",
	"ma hang",
	"item",
	"hàng hóa",
	"hang hoa",
}


def get_stock_context(question):
	if not _looks_like_stock_question(question):
		return ""

	if not frappe.has_permission("Item", "read"):
		return "Dữ liệu ERPNext liên quan:\n- Người dùng không có quyền đọc Hàng hóa."

	items = _find_items(question)
	if not items:
		return (
			"Dữ liệu ERPNext liên quan:\n"
			"- Không tìm thấy hàng hóa phù hợp trong câu hỏi.\n"
			"- Hãy hỏi kèm mã hàng hoặc tên hàng cụ thể."
		)

	lines = ["Dữ liệu ERPNext liên quan tới hàng hóa và tồn kho:"]
	for item in items[:MAX_ITEMS]:
		lines.extend(_get_item_lines(item))
		lines.extend(_get_bin_lines(item["name"]))

	return "\n".join(lines)


def _looks_like_stock_question(question):
	query = _normalize(question)
	return any(keyword in query for keyword in STOCK_KEYWORDS)


def _find_items(question):
	candidates = _extract_item_candidates(question)
	filters = []

	for candidate in candidates:
		filters.append(["item_code", "like", f"%{candidate}%"])
		filters.append(["item_name", "like", f"%{candidate}%"])

	if not filters:
		return []

	# Frappe OR filters are explicit via or_filters; keep selected fields small.
	items = frappe.get_list(
		"Item",
		or_filters=filters,
		fields=["name", "item_code", "item_name", "item_group", "stock_uom", "is_stock_item", "disabled"],
		limit_page_length=MAX_ITEMS,
		order_by="modified desc",
	)
	return items


def _extract_item_candidates(question):
	raw = str(question or "")
	candidates = []

	quoted = re.findall(r"[\"'“”‘’]([^\"'“”‘’]{2,80})[\"'“”‘’]", raw)
	candidates.extend(quoted)

	uppercase_codes = re.findall(r"\b[A-Z0-9][A-Z0-9._/-]{2,}\b", raw)
	candidates.extend(uppercase_codes)

	query = _normalize(raw)
	for marker in [
		"mã hàng",
		"ma hang",
		"item",
		"hàng",
		"hang",
		"tồn kho",
		"ton kho",
		"còn bao nhiêu",
		"con bao nhieu",
		"còn hàng",
		"con hang",
		"số lượng tồn",
		"so luong ton",
	]:
		if marker in query:
			after = query.split(marker, 1)[1].strip(" :.-")
			if after:
				candidates.append(" ".join(after.split()[:5]))

	seen = set()
	result = []
	for candidate in candidates:
		candidate = candidate.strip()
		key = candidate.casefold()
		if len(candidate) < 2 or key in seen:
			continue
		seen.add(key)
		result.append(candidate[:80])

	return result[:6]


def _get_item_lines(item):
	return [
		f"- Hàng hóa: {item.get('item_code') or item.get('name')} - {item.get('item_name') or ''}",
		f"  Nhóm hàng: {item.get('item_group') or ''}",
		f"  Đơn vị tồn kho: {item.get('stock_uom') or ''}",
		f"  Theo dõi tồn kho: {'Có' if item.get('is_stock_item') else 'Không'}",
		f"  Trạng thái: {'Đã tắt' if item.get('disabled') else 'Đang dùng'}",
	]


def _get_bin_lines(item_code):
	if not frappe.has_permission("Bin", "read"):
		return ["  Tồn kho: người dùng không có quyền đọc Bin."]

	bins = frappe.get_list(
		"Bin",
		filters={"item_code": item_code},
		fields=["warehouse", "actual_qty", "projected_qty", "reserved_qty", "ordered_qty"],
		limit_page_length=MAX_BINS_PER_ITEM,
		order_by="actual_qty desc",
	)
	if not bins:
		return ["  Tồn kho: chưa có số liệu tồn theo kho."]

	lines = ["  Tồn theo kho:"]
	total_actual = 0
	for row in bins:
		total_actual += row.get("actual_qty") or 0
		lines.append(
			"  - {warehouse}: tồn thực tế {actual_qty}, dự kiến {projected_qty}".format(
				warehouse=row.get("warehouse"),
				actual_qty=_format_number(row.get("actual_qty")),
				projected_qty=_format_number(row.get("projected_qty")),
			)
		)
	lines.append(f"  Tổng tồn thực tế trong các kho trên: {_format_number(total_actual)}")
	return lines


def _format_number(value):
	if value is None:
		return "0"
	return f"{value:g}" if isinstance(value, int | float) else str(value)


def _normalize(text):
	return str(text or "").casefold()
