"""Regional defaults for Vietnamese deployments."""

import frappe


def sync_vn_regional_settings():
    current_language = frappe.db.get_single_value("System Settings", "language")
    if not current_language or current_language == "en":
        frappe.db.set_single_value("System Settings", "language", "vi", update_modified=False)
