"""Ensure VND currency is enabled and correctly configured."""

import frappe


def sync_vnd_currency():
    if not frappe.db.exists("DocType", "Currency"):
        return

    if frappe.db.exists("Currency", "VND"):
        frappe.db.set_value("Currency", "VND", {
            "enabled": 1,
            "symbol": "₫",
            "fraction": "Xu",
            "fraction_units": 100,
            "number_format": "#.###",
            "smallest_currency_fraction_value": 0,
        }, update_modified=False)
    else:
        doc = frappe.get_doc({
            "doctype": "Currency",
            "currency_name": "VND",
            "enabled": 1,
            "symbol": "₫",
            "fraction": "Xu",
            "fraction_units": 100,
            "number_format": "#.###",
            "smallest_currency_fraction_value": 0,
        })
        doc.insert(ignore_permissions=True)
