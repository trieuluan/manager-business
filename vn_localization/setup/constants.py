"""Constants used by vn_localization setup services."""

APP_MODULE = "Vn Localization"
APP_NAME = "vn_localization"

VN_SME_ACCOUNTS = {
    "Asset": [
        {"account_name": "Tiền mặt", "account_number": "111", "account_type": "Cash"},
        {"account_name": "Tiền gửi ngân hàng", "account_number": "112", "account_type": "Bank"},
        {"account_name": "Phải thu khách hàng", "account_number": "131", "account_type": "Receivable"},
        {"account_name": "Thuế GTGT được khấu trừ", "account_number": "1331", "account_type": "Tax"},
        {"account_name": "Phải thu khác", "account_number": "138", "account_type": "Current Asset"},
        {"account_name": "Nguyên vật liệu", "account_number": "152", "account_type": "Current Asset"},
        {"account_name": "Công cụ dụng cụ", "account_number": "153", "account_type": "Current Asset"},
        {"account_name": "Thành phẩm", "account_number": "155", "account_type": "Stock"},
        {"account_name": "Hàng hóa", "account_number": "156", "account_type": "Stock"},
    ],
    "Liability": [
        {"account_name": "Phải trả nhà cung cấp", "account_number": "331", "account_type": "Payable"},
        {"account_name": "Thuế GTGT phải nộp", "account_number": "3331", "account_type": "Tax"},
        {"account_name": "Phải trả người lao động", "account_number": "334", "account_type": "Current Liability"},
        {"account_name": "Phải trả khác", "account_number": "338", "account_type": "Current Liability"},
    ],
    "Equity": [
        {"account_name": "Vốn đầu tư của chủ sở hữu", "account_number": "411", "account_type": "Equity"},
        {
            "account_name": "Lợi nhuận sau thuế chưa phân phối",
            "account_number": "421",
            "account_type": "Equity",
        },
    ],
    "Income": [
        {"account_name": "Doanh thu bán hàng", "account_number": "511", "account_type": "Income Account"},
        {"account_name": "Doanh thu tài chính", "account_number": "515", "account_type": "Indirect Income"},
        {"account_name": "Thu nhập khác", "account_number": "711", "account_type": "Indirect Income"},
    ],
    "Expense": [
        {"account_name": "Giá vốn hàng bán", "account_number": "632", "account_type": "Cost of Goods Sold"},
        {"account_name": "Chi phí tài chính", "account_number": "635", "account_type": "Indirect Expense"},
        {"account_name": "Chi phí bán hàng", "account_number": "641", "account_type": "Indirect Expense"},
        {
            "account_name": "Chi phí quản lý doanh nghiệp",
            "account_number": "642",
            "account_type": "Indirect Expense",
        },
        {"account_name": "Chi phí khác", "account_number": "811", "account_type": "Indirect Expense"},
    ],
}


VN_PRINT_FORMATS = [
    {
        "name": "VN Sales Invoice",
        "doc_type": "Sales Invoice",
        "title": "Hóa đơn bán hàng",
        "party_label": "Khách hàng",
        "party_field": "customer_name",
        "date_field": "posting_date",
    },
    {
        "name": "VN Sales Order",
        "doc_type": "Sales Order",
        "title": "Đơn bán hàng",
        "party_label": "Khách hàng",
        "party_field": "customer_name",
        "date_field": "transaction_date",
    },
    {
        "name": "VN Purchase Invoice",
        "doc_type": "Purchase Invoice",
        "title": "Hóa đơn mua hàng",
        "party_label": "Nhà cung cấp",
        "party_field": "supplier_name",
        "date_field": "posting_date",
    },
    {
        "name": "VN Delivery Note",
        "doc_type": "Delivery Note",
        "title": "Phiếu giao hàng",
        "party_label": "Khách hàng",
        "party_field": "customer_name",
        "date_field": "posting_date",
    },
    {
        "name": "VN Purchase Receipt",
        "doc_type": "Purchase Receipt",
        "title": "Phiếu nhập hàng",
        "party_label": "Nhà cung cấp",
        "party_field": "supplier_name",
        "date_field": "posting_date",
    },
]
