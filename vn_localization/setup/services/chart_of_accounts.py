"""Seed common Vietnamese SME accounts under existing company roots."""

import frappe

from vn_localization.setup.constants import VN_SME_ACCOUNTS


def sync_vn_chart_of_accounts():
    if not frappe.db.exists("DocType", "Company"):
        return

    companies = frappe.get_all("Company", pluck="name")
    for company in companies:
        for root_type, accounts in VN_SME_ACCOUNTS.items():
            parent_account = _get_root_account(company, root_type)
            if not parent_account:
                continue

            for account in accounts:
                _ensure_account(company, parent_account, root_type, account)


def _get_root_account(company, root_type):
    roots = frappe.get_all(
        "Account",
        filters={"company": company, "root_type": root_type, "parent_account": ["is", "not set"]},
        pluck="name",
        order_by="lft asc",
        limit_page_length=1,
    )
    return roots[0] if roots else None


def _ensure_account(company, parent_account, root_type, account):
    existing = frappe.get_all(
        "Account",
        filters={"company": company, "account_number": account["account_number"]},
        pluck="name",
        limit_page_length=1,
    )
    if existing:
        return existing[0]

    report_type = "Balance Sheet" if root_type in {"Asset", "Liability", "Equity"} else "Profit and Loss"
    company_currency = frappe.get_cached_value("Company", company, "default_currency")

    doc = frappe.get_doc(
        {
            "doctype": "Account",
            "account_name": account["account_name"],
            "account_number": account["account_number"],
            "company": company,
            "parent_account": parent_account,
            "is_group": 0,
            "root_type": root_type,
            "report_type": report_type,
            "account_type": account.get("account_type"),
            "account_currency": company_currency,
        }
    )
    doc.flags.ignore_permissions = True
    doc.insert()
    return doc.name
