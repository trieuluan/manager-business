"""Apply Vietnamese defaults to all companies."""

import frappe


def sync_vn_company_defaults():
    if not frappe.db.exists("DocType", "Company"):
        return

    companies = frappe.get_all("Company", fields=["name", "abbr", "default_currency"])
    for company in companies:
        _apply_defaults(company)


def _apply_defaults(company):
    updates = {}

    if not company.get("default_currency"):
        updates["default_currency"] = "VND"

    default_receivable = frappe.db.get_value(
        "Account",
        {"company": company["name"], "account_number": "131", "account_type": "Receivable"},
        "name",
    )
    if default_receivable:
        updates["default_receivable_account"] = default_receivable

    default_payable = frappe.db.get_value(
        "Account",
        {"company": company["name"], "account_number": "331", "account_type": "Payable"},
        "name",
    )
    if default_payable:
        updates["default_payable_account"] = default_payable

    if updates:
        frappe.db.set_value("Company", company["name"], updates, update_modified=False)
