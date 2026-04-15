"""Language synchronization helpers."""

import frappe


def sync_vietnamese_language():
    name = frappe.db.exists("Language", {"language_code": "vi"}) or frappe.db.exists("Language", "vi")

    if name:
        frappe.db.set_value("Language", name, "enabled", 1, update_modified=False)
        return name

    doc = frappe.get_doc(
        {
            "doctype": "Language",
            "language_code": "vi",
            "language_name": "Tiếng Việt",
            "enabled": 1,
        }
    )
    doc.insert(ignore_permissions=True)
    return doc.name
