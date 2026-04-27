"""Lightweight documentation retrieval for the local AI assistant."""

from __future__ import annotations

from pathlib import Path

import frappe


DOCS_DIR = Path(__file__).resolve().parent / "docs"
MAX_CONTEXT_CHARS = 3000

DOC_SYNONYMS = {
	"payment_entry": [
		"thu tiền", "chi tiền", "thanh toán", "phiếu thu", "phiếu chi",
		"thu tien", "chi tien", "thanh toan", "phieu thu", "phieu chi",
		"payment", "collect", "pay",
	],
	"sales_invoice": [
		"hóa đơn bán", "xuất hóa đơn", "lập hóa đơn", "hóa đơn khách",
		"hoa don ban", "xuat hoa don", "lap hoa don",
		"invoice", "billing",
	],
	"purchase_invoice": [
		"hóa đơn mua", "hóa đơn nhà cung cấp", "hóa đơn ncc",
		"hoa don mua", "hoa don ncc",
		"purchase invoice", "vendor invoice",
	],
	"purchase_order": [
		"đơn mua hàng", "đặt hàng nhà cung cấp", "đơn đặt hàng mua",
		"don mua hang", "dat hang ncc",
		"purchase order", "po",
	],
	"sales_order": [
		"đơn bán hàng", "đơn hàng khách", "xác nhận đơn hàng",
		"don ban hang", "don hang khach",
		"sales order", "so",
	],
	"stock": [
		"tồn kho", "nhập kho", "xuất kho", "chuyển kho", "kiểm kê",
		"ton kho", "nhap kho", "xuat kho", "chuyen kho", "kiem ke",
		"stock", "warehouse", "inventory", "kho hàng",
	],
	"accounting": [
		"bút toán", "hạch toán", "sổ cái", "công nợ", "kế toán",
		"but toan", "hach toan", "so cai", "cong no", "ke toan",
		"journal", "ledger", "accounting", "balance sheet", "lãi lỗ",
	],
	"reports": [
		"báo cáo", "thống kê", "doanh thu", "bảng cân đối", "kết quả kinh doanh",
		"bao cao", "thong ke", "doanh thu", "bang can doi",
		"report", "analytics", "statement",
	],
	"delivery_note": [
		"giao hàng", "phiếu giao hàng", "xuất hàng cho khách",
		"giao hang", "phieu giao hang",
		"delivery", "shipment",
	],
	"quotation": [
		"báo giá", "lập báo giá", "gửi báo giá",
		"bao gia", "lap bao gia",
		"quote", "quotation",
	],
	"material_request": [
		"yêu cầu mua", "đề nghị mua", "yêu cầu vật tư",
		"yeu cau mua", "de nghi mua",
		"material request", "purchase request",
	],
}


def get_relevant_context(question):
	question_lower = (question or "").lower()
	docs = []

	for path in sorted(DOCS_DIR.glob("*.md")):
		content = path.read_text(encoding="utf-8")
		score = _score_doc(question_lower, path.stem, content)
		if score:
			docs.append((score, path.stem, content))

	if not docs:
		return ""

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


def _score_doc(question, stem, content):
	score = 0
	text = content.lower()
	tokens = _tokens(question)

	# token match trong content
	for token in tokens:
		if token in text:
			score += 1

	# synonym boost — match trực tiếp vào doc đúng
	for synonyms in DOC_SYNONYMS.get(stem, []):
		if synonyms in question:
			score += 5

	# title/stem match
	stem_normalized = stem.replace("_", " ")
	if stem_normalized in question or stem in question:
		score += 3

	return score


def _tokens(text):
	return [token.strip(".,:;!?()[]{}\"'") for token in text.split() if len(token.strip()) >= 3]
