"""Seed Vietnamese modes of payment."""

import frappe

VN_MODES_OF_PAYMENT = [
    {"mode_of_payment": "Tiền mặt", "type": "Cash"},
    {"mode_of_payment": "Chuyển khoản ngân hàng", "type": "Bank"},
    {"mode_of_payment": "Ví điện tử", "type": "Bank"},
    {"mode_of_payment": "Thẻ tín dụng", "type": "Bank"},
    {"mode_of_payment": "Séc", "type": "Bank"},
]


def sync_vn_modes_of_payment():
    if not frappe.db.exists("DocType", "Mode of Payment"):
        return

    for mop in VN_MODES_OF_PAYMENT:
        if frappe.db.exists("Mode of Payment", mop["mode_of_payment"]):
            continue
        doc = frappe.get_doc({
            "doctype": "Mode of Payment",
            "mode_of_payment": mop["mode_of_payment"],
            "type": mop["type"],
        })
        doc.insert(ignore_permissions=True)
