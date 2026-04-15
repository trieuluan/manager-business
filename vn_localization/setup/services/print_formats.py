"""Basic Vietnamese print format seeds."""

import frappe

from vn_localization.setup.constants import APP_MODULE, VN_PRINT_FORMATS


def sync_vn_print_defaults():
    for config in VN_PRINT_FORMATS:
        doc_type = config.get("doc_type")
        if doc_type and not frappe.db.exists("DocType", doc_type):
            continue
        _upsert_print_format(config)


def _upsert_print_format(config):
    doc_type = config.get("doc_type")
    if doc_type and not frappe.db.exists("DocType", doc_type):
        return None
    
    existing_name = frappe.db.exists("Print Format", config["name"])
    values = {
        "doctype": "Print Format",
        "name": config["name"],
        "module": APP_MODULE,
        "doc_type": doc_type,
        "print_format_type": "Jinja",
        "print_format_for": "DocType",
        "custom_format": 1,
        "disabled": 0,
        "default_print_language": "vi",
        "html": _build_template(config),
    }

    if existing_name:
        doc = frappe.get_doc("Print Format", existing_name)
        doc.update(values)
        doc.save(ignore_permissions=True)
        return doc.name

    doc = frappe.get_doc(values)
    doc.insert(ignore_permissions=True)
    return doc.name


def _build_template(config):
    party_label = config["party_label"]
    party_field = config["party_field"]
    date_field = config["date_field"]
    title = config["title"]

    return f"""
<div class="print-format">
    <h2 style="margin-bottom: 8px;">{title}</h2>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 16px;">
        <tr>
            <td style="padding: 6px 0;"><strong>Số chứng từ:</strong> {{{{ doc.name }}}}</td>
            <td style="padding: 6px 0; text-align: right;"><strong>Ngày:</strong> {{{{ frappe.utils.format_date(doc.get("{date_field}")) }}}}</td>
        </tr>
        <tr>
            <td colspan="2" style="padding: 6px 0;"><strong>{party_label}:</strong> {{{{ doc.get("{party_field}") or "" }}}}</td>
        </tr>
    </table>

    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr>
                <th style="border: 1px solid #d1d5db; padding: 8px;">STT</th>
                <th style="border: 1px solid #d1d5db; padding: 8px; text-align: left;">Mặt hàng</th>
                <th style="border: 1px solid #d1d5db; padding: 8px;">ĐVT</th>
                <th style="border: 1px solid #d1d5db; padding: 8px; text-align: right;">Số lượng</th>
                <th style="border: 1px solid #d1d5db; padding: 8px; text-align: right;">Đơn giá</th>
                <th style="border: 1px solid #d1d5db; padding: 8px; text-align: right;">Thành tiền</th>
            </tr>
        </thead>
        <tbody>
            {{% for item in doc.items %}}
            <tr>
                <td style="border: 1px solid #d1d5db; padding: 8px; text-align: center;">{{{{ loop.index }}}}</td>
                <td style="border: 1px solid #d1d5db; padding: 8px;">{{{{ item.item_name or item.item_code or "" }}}}</td>
                <td style="border: 1px solid #d1d5db; padding: 8px; text-align: center;">{{{{ item.uom or "" }}}}</td>
                <td style="border: 1px solid #d1d5db; padding: 8px; text-align: right;">{{{{ item.get_formatted("qty", doc) if item.get("qty") is not none else "" }}}}</td>
                <td style="border: 1px solid #d1d5db; padding: 8px; text-align: right;">{{{{ item.get_formatted("rate", doc) if item.get("rate") is not none else "" }}}}</td>
                <td style="border: 1px solid #d1d5db; padding: 8px; text-align: right;">{{{{ item.get_formatted("amount", doc) if item.get("amount") is not none else "" }}}}</td>
            </tr>
            {{% endfor %}}
        </tbody>
    </table>

    {{% if doc.get("grand_total") is not none %}}
    <table style="width: 100%; margin-top: 16px;">
        <tr>
            <td style="text-align: right;"><strong>Tổng thanh toán:</strong> {{{{ doc.get_formatted("grand_total", doc) }}}}</td>
        </tr>
    </table>
    {{% endif %}}

    {{% if doc.get("in_words") %}}
    <p style="margin-top: 12px;"><strong>Bằng chữ:</strong> {{{{ doc.in_words }}}}</p>
    {{% endif %}}
</div>
""".strip()
