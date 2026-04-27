"""Seed Vietnamese construction material UOMs."""

import frappe

VN_UOMS = [
    {"uom_name": "m²", "must_be_whole_number": 0},
    {"uom_name": "m³", "must_be_whole_number": 0},
    {"uom_name": "Tấn", "must_be_whole_number": 0},
    {"uom_name": "Bao", "must_be_whole_number": 1},
    {"uom_name": "Thanh", "must_be_whole_number": 1},
    {"uom_name": "Tấm", "must_be_whole_number": 1},
    {"uom_name": "Cuộn", "must_be_whole_number": 1},
    {"uom_name": "Viên", "must_be_whole_number": 1},
    {"uom_name": "Thùng", "must_be_whole_number": 1},
    {"uom_name": "Chai", "must_be_whole_number": 1},
    {"uom_name": "Lon", "must_be_whole_number": 1},
    {"uom_name": "Gói", "must_be_whole_number": 1},
    {"uom_name": "Ống", "must_be_whole_number": 1},
    {"uom_name": "Cây", "must_be_whole_number": 1},
]

VN_UOMS_ENABLED = [
    "Nos", "Box", "Kg", "Gram", "Meter", "Liter", "Pair", "Set",
    "Dozen", "Hour", "Day", "Month", "Unit", "Piece", "Roll", "Sheet",
    "Bag", "Bottle", "Can", "Pack", "Carton", "Tube", "Tonne",
    # VN custom
    "m²", "m³", "Tấn", "Bao", "Thanh", "Tấm", "Cuộn", "Viên",
    "Thùng", "Chai", "Lon", "Gói", "Ống", "Cây",
]


def sync_vn_uoms():
    if not frappe.db.exists("DocType", "UOM"):
        return

    for uom in VN_UOMS:
        if frappe.db.exists("UOM", uom["uom_name"]):
            continue
        doc = frappe.get_doc({"doctype": "UOM", **uom})
        doc.insert(ignore_permissions=True)

    frappe.db.sql(
        "UPDATE `tabUOM` SET enabled = 0 WHERE uom_name NOT IN ({})".format(
            ", ".join(["%s"] * len(VN_UOMS_ENABLED))
        ),
        VN_UOMS_ENABLED,
    )
