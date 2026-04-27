"""Seed Vietnamese supplier and customer groups."""

import frappe

VN_SUPPLIER_GROUPS = [
    {"supplier_group_name": "Nhà sản xuất", "parent_supplier_group": "All Supplier Groups"},
    {"supplier_group_name": "Nhà phân phối", "parent_supplier_group": "All Supplier Groups"},
    {"supplier_group_name": "Đại lý", "parent_supplier_group": "All Supplier Groups"},
]

VN_CUSTOMER_GROUPS = [
    {"customer_group_name": "Nhà thầu", "parent_customer_group": "All Customer Groups"},
    {"customer_group_name": "Đại lý", "parent_customer_group": "All Customer Groups"},
    {"customer_group_name": "Khách lẻ", "parent_customer_group": "All Customer Groups"},
    {"customer_group_name": "Doanh nghiệp", "parent_customer_group": "All Customer Groups"},
]


def sync_vn_party_groups():
    _sync_supplier_groups()
    _sync_customer_groups()


def _sync_supplier_groups():
    if not frappe.db.exists("DocType", "Supplier Group"):
        return
    for group in VN_SUPPLIER_GROUPS:
        if frappe.db.exists("Supplier Group", group["supplier_group_name"]):
            continue
        doc = frappe.get_doc({"doctype": "Supplier Group", **group})
        doc.insert(ignore_permissions=True)


def _sync_customer_groups():
    if not frappe.db.exists("DocType", "Customer Group"):
        return
    for group in VN_CUSTOMER_GROUPS:
        if frappe.db.exists("Customer Group", group["customer_group_name"]):
            continue
        doc = frappe.get_doc({"doctype": "Customer Group", **group})
        doc.insert(ignore_permissions=True)
