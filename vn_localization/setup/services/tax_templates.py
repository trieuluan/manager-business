"""Seed Vietnamese VAT tax templates."""

import frappe


VN_TAX_TEMPLATES = [
    {
        "name": "VAT 10% - Đầu ra",
        "tax_type": "Sales",
        "rate": 10.0,
        "account_head_type": "Tax",
        "description": "Thuế GTGT đầu ra 10%",
        "account_name": "Thuế GTGT phải nộp",
        "account_number": "3331",
    },
    {
        "name": "VAT 8% - Đầu ra",
        "tax_type": "Sales",
        "rate": 8.0,
        "account_head_type": "Tax",
        "description": "Thuế GTGT đầu ra 8%",
        "account_name": "Thuế GTGT phải nộp",
        "account_number": "3331",
    },
    {
        "name": "VAT 10% - Đầu vào",
        "tax_type": "Purchase",
        "rate": 10.0,
        "account_head_type": "Tax",
        "description": "Thuế GTGT đầu vào 10%",
        "account_name": "Thuế GTGT được khấu trừ",
        "account_number": "1331",
    },
    {
        "name": "VAT 8% - Đầu vào",
        "tax_type": "Purchase",
        "rate": 8.0,
        "account_head_type": "Tax",
        "description": "Thuế GTGT đầu vào 8%",
        "account_name": "Thuế GTGT được khấu trừ",
        "account_number": "1331",
    },
]


def sync_vn_tax_templates():
    if not frappe.db.exists("DocType", "Sales Taxes and Charges Template"):
        return

    companies = frappe.get_all("Company", pluck="name")
    for company in companies:
        for tmpl in VN_TAX_TEMPLATES:
            _upsert_tax_template(company, tmpl)


def _upsert_tax_template(company, tmpl):
    doctype = "Sales Taxes and Charges Template" if tmpl["tax_type"] == "Sales" else "Purchase Taxes and Charges Template"
    charge_doctype = "Sales Taxes and Charges" if tmpl["tax_type"] == "Sales" else "Purchase Taxes and Charges"

    if frappe.db.exists(doctype, {"title": tmpl["name"], "company": company}):
        return

    account_head = frappe.db.get_value(
        "Account",
        {"company": company, "account_number": tmpl["account_number"]},
        "name",
    )
    if not account_head:
        return

    doc = frappe.get_doc({
        "doctype": doctype,
        "title": tmpl["name"],
        "company": company,
        "taxes": [{
            "doctype": charge_doctype,
            "charge_type": "On Net Total",
            "account_head": account_head,
            "description": tmpl["description"],
            "rate": tmpl["rate"],
        }],
    })
    doc.insert(ignore_permissions=True)
