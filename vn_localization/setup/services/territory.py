"""Seed Vietnamese territories."""

import frappe

VN_TERRITORIES = [
    {"territory_name": "Việt Nam", "parent_territory": "All Territories", "children": [
        "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Hải Phòng", "Cần Thơ",
        "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu",
        "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước",
        "Bình Thuận", "Cà Mau", "Cao Bằng", "Đắk Lắk", "Đắk Nông",
        "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",
        "Hà Nam", "Hà Tĩnh", "Hải Dương", "Hậu Giang", "Hòa Bình",
        "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu",
        "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định",
        "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên",
        "Quảng Bình", "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị",
        "Sóc Trăng", "Sơn La", "Tây Ninh", "Thái Bình", "Thái Nguyên",
        "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang", "Trà Vinh", "Tuyên Quang",
        "Vĩnh Long", "Vĩnh Phúc", "Yên Bái",
    ]},
]


def sync_vn_territories():
    if not frappe.db.exists("DocType", "Territory"):
        return

    for group in VN_TERRITORIES:
        parent_name = group["territory_name"]
        if not frappe.db.exists("Territory", parent_name):
            doc = frappe.get_doc({
                "doctype": "Territory",
                "territory_name": parent_name,
                "parent_territory": group["parent_territory"],
                "is_group": 1,
            })
            doc.insert(ignore_permissions=True)

        for child in group["children"]:
            if frappe.db.exists("Territory", child):
                continue
            doc = frappe.get_doc({
                "doctype": "Territory",
                "territory_name": child,
                "parent_territory": parent_name,
                "is_group": 0,
            })
            doc.insert(ignore_permissions=True)
