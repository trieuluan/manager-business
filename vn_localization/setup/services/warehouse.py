"""Seed default Vietnamese warehouses per company."""

import frappe

VN_WAREHOUSES = [
    {"warehouse_name": "Kho chính", "warehouse_type": "Transit"},
    {"warehouse_name": "Kho hàng trả", "warehouse_type": "Transit"},
]


def sync_vn_warehouses():
    if not frappe.db.exists("DocType", "Warehouse"):
        return

    companies = frappe.get_all("Company", fields=["name", "abbr"])
    for company in companies:
        for wh in VN_WAREHOUSES:
            full_name = f"{wh['warehouse_name']} - {company['abbr']}"
            if frappe.db.exists("Warehouse", full_name):
                continue
            doc = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": wh["warehouse_name"],
                "company": company["name"],
                "is_group": 0,
            })
            doc.insert(ignore_permissions=True)
