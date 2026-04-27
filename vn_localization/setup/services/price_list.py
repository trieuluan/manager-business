"""Seed Vietnamese price lists."""

import frappe

VN_PRICE_LISTS = [
    {"price_list_name": "Bảng giá bán lẻ", "selling": 1, "buying": 0, "currency": "VND"},
    {"price_list_name": "Bảng giá bán buôn", "selling": 1, "buying": 0, "currency": "VND"},
    {"price_list_name": "Bảng giá mua vào", "selling": 0, "buying": 1, "currency": "VND"},
]


def sync_vn_price_lists():
    if not frappe.db.exists("DocType", "Price List"):
        return

    for pl in VN_PRICE_LISTS:
        if frappe.db.exists("Price List", pl["price_list_name"]):
            continue
        doc = frappe.get_doc({"doctype": "Price List", **pl})
        doc.insert(ignore_permissions=True)
