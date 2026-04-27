"""Workspace sidebar context for Vietnamese menu-aware answers."""

from __future__ import annotations

import json
from pathlib import Path

import frappe


SIDEBAR_NAME = "Trang chủ VN"
SIDEBAR_JSON = Path(__file__).resolve().parents[1] / "workspace_sidebar" / "trang_chủ_vn.json"
MAX_MENU_MATCHES = 8

MENU_SYNONYMS = {
	"yêu cầu mua": ["Material Request", "Yêu cầu mua"],
	"yeu cau mua": ["Material Request", "Yêu cầu mua"],
	"đề nghị mua": ["Material Request", "Yêu cầu mua"],
	"de nghi mua": ["Material Request", "Yêu cầu mua"],
	"yêu cầu báo giá": ["Request for Quotation", "Yêu cầu báo giá"],
	"yeu cau bao gia": ["Request for Quotation", "Yêu cầu báo giá"],
	"báo giá nhà cung cấp": ["Supplier Quotation", "Báo giá từ NCC"],
	"bao gia nha cung cap": ["Supplier Quotation", "Báo giá từ NCC"],
	"báo giá từ ncc": ["Supplier Quotation", "Báo giá từ NCC"],
	"bao gia tu ncc": ["Supplier Quotation", "Báo giá từ NCC"],
	"đơn mua hàng": ["Purchase Order", "Đơn đặt hàng"],
	"don mua hang": ["Purchase Order", "Đơn đặt hàng"],
	"đơn đặt hàng": ["Purchase Order", "Đơn đặt hàng"],
	"don dat hang": ["Purchase Order", "Đơn đặt hàng"],
	"nhập hàng": ["Purchase Receipt", "Phiếu nhập kho"],
	"nhap hang": ["Purchase Receipt", "Phiếu nhập kho"],
	"nhập kho mua hàng": ["Purchase Receipt", "Phiếu nhập kho"],
	"nhap kho mua hang": ["Purchase Receipt", "Phiếu nhập kho"],
	"hóa đơn bán hàng": ["Sales Invoice", "sales invoice"],
	"hoa don ban hang": ["Sales Invoice", "sales invoice"],
	"xuất hóa đơn": ["Sales Invoice", "Hóa đơn bán hàng"],
	"xuat hoa don": ["Sales Invoice", "Hóa đơn bán hàng"],
	"lập hóa đơn": ["Sales Invoice", "Hóa đơn bán hàng"],
	"lap hoa don": ["Sales Invoice", "Hóa đơn bán hàng"],
	"hóa đơn mua hàng": ["Purchase Invoice", "purchase invoice"],
	"hoa don mua hang": ["Purchase Invoice", "purchase invoice"],
	"báo giá bán hàng": ["Quotation", "Báo giá"],
	"bao gia ban hang": ["Quotation", "Báo giá"],
	"báo giá khách hàng": ["Quotation", "Báo giá"],
	"bao gia khach hang": ["Quotation", "Báo giá"],
	"đơn bán hàng": ["Sales Order", "Đơn bán hàng"],
	"don ban hang": ["Sales Order", "Đơn bán hàng"],
	"giao hàng": ["Delivery Note", "Phiếu giao hàng"],
	"giao hang": ["Delivery Note", "Phiếu giao hàng"],
	"phiếu giao hàng": ["Delivery Note", "Phiếu giao hàng"],
	"phieu giao hang": ["Delivery Note", "Phiếu giao hàng"],
	"sổ bán hàng": ["Sales Register", "Sổ bán hàng"],
	"so ban hang": ["Sales Register", "Sổ bán hàng"],
	"báo cáo bán hàng": ["Sales Register", "Sổ bán hàng"],
	"bao cao ban hang": ["Sales Register", "Sổ bán hàng"],
	"phiếu thu chi": ["Payment Entry", "payment entry"],
	"phieu thu chi": ["Payment Entry", "payment entry"],
	"thu tiền": ["Payment Entry", "Phiếu thu chi"],
	"thu tien": ["Payment Entry", "Phiếu thu chi"],
	"chi tiền": ["Payment Entry", "Phiếu thu chi"],
	"chi tien": ["Payment Entry", "Phiếu thu chi"],
	"thanh toán": ["Payment Entry", "Phiếu thu chi"],
	"thanh toan": ["Payment Entry", "Phiếu thu chi"],
	"bút toán": ["Journal Entry", "Bút toán"],
	"but toan": ["Journal Entry", "Bút toán"],
	"hạch toán": ["Journal Entry", "Bút toán"],
	"hach toan": ["Journal Entry", "Bút toán"],
	"công nợ phải thu": ["Accounts Receivable", "Công nợ phải thu"],
	"cong no phai thu": ["Accounts Receivable", "Công nợ phải thu"],
	"công nợ khách hàng": ["Accounts Receivable", "Công nợ phải thu"],
	"cong no khach hang": ["Accounts Receivable", "Công nợ phải thu"],
	"khách còn nợ": ["Accounts Receivable", "Công nợ phải thu"],
	"khach con no": ["Accounts Receivable", "Công nợ phải thu"],
	"công nợ phải trả": ["Accounts Payable", "Công nợ phải trả"],
	"cong no phai tra": ["Accounts Payable", "Công nợ phải trả"],
	"công nợ nhà cung cấp": ["Accounts Payable", "Công nợ phải trả"],
	"cong no nha cung cap": ["Accounts Payable", "Công nợ phải trả"],
	"nợ nhà cung cấp": ["Accounts Payable", "Công nợ phải trả"],
	"no nha cung cap": ["Accounts Payable", "Công nợ phải trả"],
	"sổ cái": ["General Ledger", "Sổ cái"],
	"so cai": ["General Ledger", "Sổ cái"],
	"bảng cân đối": ["Balance Sheet", "Bảng cân đối kế toán"],
	"bang can doi": ["Balance Sheet", "Bảng cân đối kế toán"],
	"báo cáo lãi lỗ": ["Profit and Loss Statement", "Kết quả kinh doanh"],
	"bao cao lai lo": ["Profit and Loss Statement", "Kết quả kinh doanh"],
	"kết quả kinh doanh": ["Profit and Loss Statement", "Kết quả kinh doanh"],
	"ket qua kinh doanh": ["Profit and Loss Statement", "Kết quả kinh doanh"],
	"xuất nhập kho": ["Stock Entry", "Xuất nhập kho"],
	"xuat nhap kho": ["Stock Entry", "Xuất nhập kho"],
	"chuyển kho": ["Stock Entry", "Xuất nhập kho"],
	"chuyen kho": ["Stock Entry", "Xuất nhập kho"],
	"xuất kho": ["Stock Entry", "Xuất nhập kho"],
	"xuat kho": ["Stock Entry", "Xuất nhập kho"],
	"kiểm kê kho": ["Stock Reconciliation", "Kiểm kê kho"],
	"kiem ke kho": ["Stock Reconciliation", "Kiểm kê kho"],
	"tồn kho": ["Stock Balance", "stock balance"],
	"ton kho": ["Stock Balance", "stock balance"],
	"tồn kho hiện tại": ["Stock Balance", "Tồn kho hiện tại"],
	"ton kho hien tai": ["Stock Balance", "Tồn kho hiện tại"],
	"sổ kho": ["Stock Ledger", "Sổ kho"],
	"so kho": ["Stock Ledger", "Sổ kho"],
	"lô hàng": ["Batch", "Lô hàng"],
	"lo hang": ["Batch", "Lô hàng"],
	"serial": ["Serial No", "Số serial"],
	"số serial": ["Serial No", "Số serial"],
	"so serial": ["Serial No", "Số serial"],
	"mặt hàng": ["Item", "item"],
	"mat hang": ["Item", "item"],
	"hàng hóa": ["Item", "Hàng hóa"],
	"hang hoa": ["Item", "Hàng hóa"],
	"nhóm hàng": ["Item Group", "Nhóm hàng hóa"],
	"nhom hang": ["Item Group", "Nhóm hàng hóa"],
	"đơn vị tính": ["UOM", "Đơn vị tính"],
	"don vi tinh": ["UOM", "Đơn vị tính"],
	"bảng giá": ["Item Price", "Bảng giá"],
	"bang gia": ["Item Price", "Bảng giá"],
	"giá bán": ["Item Price", "Bảng giá"],
	"gia ban": ["Item Price", "Bảng giá"],
	"thương hiệu": ["Brand", "Thương hiệu"],
	"thuong hieu": ["Brand", "Thương hiệu"],
	"khách hàng": ["Customer", "customer"],
	"khach hang": ["Customer", "customer"],
	"nhóm khách hàng": ["Customer Group", "Nhóm khách hàng"],
	"nhom khach hang": ["Customer Group", "Nhóm khách hàng"],
	"nhà cung cấp": ["Supplier", "supplier"],
	"nha cung cap": ["Supplier", "supplier"],
	"nhóm nhà cung cấp": ["Supplier Group", "Nhóm nhà cung cấp"],
	"nhom nha cung cap": ["Supplier Group", "Nhóm nhà cung cấp"],
	"kho hàng": ["Warehouse", "Kho"],
	"kho hang": ["Warehouse", "Kho"],
	"phương thức thanh toán": ["Mode of Payment", "Phương thức thanh toán"],
	"phuong thuc thanh toan": ["Mode of Payment", "Phương thức thanh toán"],
	"điều kiện thanh toán": ["Payment Terms Template", "Điều kiện thanh toán"],
	"dieu kien thanh toan": ["Payment Terms Template", "Điều kiện thanh toán"],
	"cài đặt kho": ["Stock Settings", "Cài đặt kho"],
	"cai dat kho": ["Stock Settings", "Cài đặt kho"],
	"cài đặt bán hàng": ["Selling Settings", "Cài đặt bán hàng"],
	"cai dat ban hang": ["Selling Settings", "Cài đặt bán hàng"],
	"cài đặt mua hàng": ["Buying Settings", "Cài đặt mua hàng"],
	"cai dat mua hang": ["Buying Settings", "Cài đặt mua hàng"],
	"cài đặt kế toán": ["Accounts Settings", "Cài đặt kế toán"],
	"cai dat ke toan": ["Accounts Settings", "Cài đặt kế toán"],
	"nhập dữ liệu": ["Data Import", "Nhập dữ liệu"],
	"nhap du lieu": ["Data Import", "Nhập dữ liệu"],
	"import dữ liệu": ["Data Import", "Nhập dữ liệu"],
	"import du lieu": ["Data Import", "Nhập dữ liệu"],
	"xuất dữ liệu": ["Data Export", "Xuất dữ liệu"],
	"xuat du lieu": ["Data Export", "Xuất dữ liệu"],
	"export dữ liệu": ["Data Export", "Xuất dữ liệu"],
	"export du lieu": ["Data Export", "Xuất dữ liệu"],
	"chỉnh sửa hàng loạt": ["Bulk Update", "Chỉnh sửa hàng loạt"],
	"chinh sua hang loat": ["Bulk Update", "Chỉnh sửa hàng loạt"],
	"thùng rác": ["Deleted Document", "Thùng rác"],
	"thung rac": ["Deleted Document", "Thùng rác"],
}


def get_menu_context(question):
	items = _get_sidebar_items()
	if not items:
		return ""

	menu_entries = _build_menu_entries(items)
	matches = _find_matches(question, menu_entries)
	if not matches:
		return _compact_menu_overview(menu_entries)

	lines = [
		"Menu bên trái đã Việt hóa:",
		"Ưu tiên hướng dẫn người dùng theo đúng đường dẫn menu bên trái dưới đây.",
	]
	for entry in matches[:MAX_MENU_MATCHES]:
		lines.append(
			f"- {entry['section']} > {entry['label']} ({entry['link_type']}: {entry['link_to']})"
		)
	return "\n".join(lines)


def _get_sidebar_items():
	try:
		if frappe.db.exists("Workspace Sidebar", SIDEBAR_NAME):
			doc = frappe.get_doc("Workspace Sidebar", SIDEBAR_NAME)
			return doc.get("items") or []
	except Exception:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI menu context DB failed")

	try:
		data = json.loads(SIDEBAR_JSON.read_text(encoding="utf-8"))
		return data.get("items") or []
	except Exception:
		frappe.log_error(frappe.get_traceback(), "vn_localization AI menu context file failed")
		return []


def _build_menu_entries(items):
	entries = []
	current_section = "Trang chủ"

	for item in items:
		label = item.get("label")
		item_type = item.get("type")
		if item_type == "Section Break" and label:
			current_section = label
			continue

		if item_type != "Link" or not label:
			continue

		entries.append(
			{
				"section": current_section,
				"label": label,
				"link_to": item.get("link_to") or "",
				"link_type": item.get("link_type") or "",
			}
		)

	return entries


def _find_matches(question, entries):
	query = _normalize(question)
	keywords = _keywords_for_query(query)
	matches = []

	for entry in entries:
		haystack = _normalize(" ".join([entry["section"], entry["label"], entry["link_to"], entry["link_type"]]))
		score = 0
		for keyword in keywords:
			if keyword and _normalize(keyword) in haystack:
				score += 3
		for token in _tokens(query):
			if token in haystack:
				score += 1
		if score:
			matches.append((score, entry))

	matches.sort(key=lambda item: item[0], reverse=True)
	return [entry for _score, entry in matches]


def _keywords_for_query(query):
	keywords = []
	for phrase, values in MENU_SYNONYMS.items():
		if _normalize(phrase) in query:
			keywords.extend(values)
	return keywords


def _compact_menu_overview(entries):
	sections = {}
	for entry in entries:
		sections.setdefault(entry["section"], []).append(entry["label"])

	lines = [
		"Menu bên trái đã Việt hóa:",
		"Chỉ dùng danh sách này để chỉ nơi mở chức năng trong menu bên trái.",
	]
	for section, labels in sections.items():
		lines.append(f"- {section}: {', '.join(labels[:8])}")
	return "\n".join(lines)


def _normalize(text):
	return str(text or "").casefold()


def _tokens(text):
	return [token.strip(".,:;!?()[]{}\"'") for token in text.split() if len(token.strip()) >= 3]
