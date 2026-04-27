"""Seed common Vietnamese payment terms."""

import frappe

VN_PAYMENT_TERMS = [
    {"payment_term_name": "Thanh toán ngay", "invoice_portion": 100.0, "credit_days": 0},
    {"payment_term_name": "Net 15 ngày", "invoice_portion": 100.0, "credit_days": 15},
    {"payment_term_name": "Net 30 ngày", "invoice_portion": 100.0, "credit_days": 30},
    {"payment_term_name": "Net 45 ngày", "invoice_portion": 100.0, "credit_days": 45},
    {"payment_term_name": "Net 60 ngày", "invoice_portion": 100.0, "credit_days": 60},
    {
        "payment_term_name": "Đặt cọc 30% - còn lại khi giao hàng",
        "invoice_portion": 30.0,
        "credit_days": 0,
    },
]


def sync_vn_payment_terms():
    if not frappe.db.exists("DocType", "Payment Term"):
        return

    for term in VN_PAYMENT_TERMS:
        if frappe.db.exists("Payment Term", term["payment_term_name"]):
            continue
        doc = frappe.get_doc({
            "doctype": "Payment Term",
            "payment_term_name": term["payment_term_name"],
            "invoice_portion": term["invoice_portion"],
            "credit_days_based_on": "Day(s) after invoice date",
            "credit_days": term["credit_days"],
        })
        doc.insert(ignore_permissions=True)
