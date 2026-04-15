"""Workspace seeds for Vietnamese SME users."""

import frappe

from vn_localization.setup.constants import APP_MODULE, APP_NAME, VN_WORKSPACES


def sync_vn_workspaces():
    if not frappe.db.exists("DocType", "Workspace"):
        return

    for config in VN_WORKSPACES:
        _upsert_workspace(config)


def _upsert_workspace(config):
    existing_name = frappe.db.exists("Workspace", config["label"])
    values = {
        "doctype": "Workspace",
        "label": config["label"],
        "title": config["title"],
        "module": APP_MODULE,
        "app": APP_NAME,
        "icon": config["icon"],
        "sequence_id": config["sequence_id"],
        "type": "Workspace",
        "public": 1,
        "is_hidden": 0,
        "hide_custom": 1,
        "content": "[]",
        "shortcuts": config["shortcuts"],
        "links": config["links"],
    }

    if existing_name:
        doc = frappe.get_doc("Workspace", existing_name)
        doc.update({k: v for k, v in values.items() if k not in {"shortcuts", "links"}})
        doc.set("shortcuts", config["shortcuts"])
        doc.set("links", config["links"])
        doc.save(ignore_permissions=True)
        return doc.name

    doc = frappe.get_doc(values)
    doc.insert(ignore_permissions=True)
    return doc.name
