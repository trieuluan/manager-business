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

VN_WORKSPACES = [
    {
        "label": "Kế toán VN",
        "title": "Kế toán VN",
        "icon": "money-coins-1",
        "sequence_id": 70.0,
        "shortcuts": [
            {"label": "Hóa đơn bán hàng", "type": "DocType", "link_to": "Sales Invoice", "doc_view": "List"},
            {"label": "Hóa đơn mua hàng", "type": "DocType", "link_to": "Purchase Invoice", "doc_view": "List"},
            {"label": "Phiếu thu chi", "type": "DocType", "link_to": "Payment Entry", "doc_view": "List"},
            {"label": "Bút toán", "type": "DocType", "link_to": "Journal Entry", "doc_view": "List"},
        ],
        "links": [
            {"type": "Card Break", "label": "Báo cáo tài chính"},
            {"type": "Link", "label": "Sổ cái", "link_type": "Report", "link_to": "General Ledger"},
            {"type": "Link", "label": "Công nợ phải thu", "link_type": "Report", "link_to": "Accounts Receivable"},
            {"type": "Link", "label": "Công nợ phải trả", "link_type": "Report", "link_to": "Accounts Payable"},
            {"type": "Link", "label": "Sơ đồ tài khoản", "link_type": "DocType", "link_to": "Account"},
        ],
    },
    {
        "label": "Bán hàng VN",
        "title": "Bán hàng VN",
        "icon": "sell",
        "sequence_id": 71.0,
        "shortcuts": [
            {"label": "Khách hàng", "type": "DocType", "link_to": "Customer", "doc_view": "List"},
            {"label": "Báo giá", "type": "DocType", "link_to": "Quotation", "doc_view": "List"},
            {"label": "Đơn bán hàng", "type": "DocType", "link_to": "Sales Order", "doc_view": "List"},
            {"label": "Hóa đơn bán hàng", "type": "DocType", "link_to": "Sales Invoice", "doc_view": "List"},
        ],
        "links": [
            {"type": "Card Break", "label": "Phát sinh bán hàng"},
            {"type": "Link", "label": "Phiếu giao hàng", "link_type": "DocType", "link_to": "Delivery Note"},
            {"type": "Link", "label": "Sổ bán hàng", "link_type": "Report", "link_to": "Sales Register"},
            {"type": "Link", "label": "Mặt hàng", "link_type": "DocType", "link_to": "Item"},
        ],
    },
    {
        "label": "Mua hàng VN",
        "title": "Mua hàng VN",
        "icon": "buying",
        "sequence_id": 72.0,
        "shortcuts": [
            {"label": "Nhà cung cấp", "type": "DocType", "link_to": "Supplier", "doc_view": "List"},
            {"label": "Yêu cầu mua", "type": "DocType", "link_to": "Material Request", "doc_view": "List"},
            {"label": "Đơn mua hàng", "type": "DocType", "link_to": "Purchase Order", "doc_view": "List"},
            {"label": "Hóa đơn mua hàng", "type": "DocType", "link_to": "Purchase Invoice", "doc_view": "List"},
        ],
        "links": [
            {"type": "Card Break", "label": "Phát sinh mua hàng"},
            {"type": "Link", "label": "Phiếu nhập mua", "link_type": "DocType", "link_to": "Purchase Receipt"},
            {"type": "Link", "label": "Mặt hàng", "link_type": "DocType", "link_to": "Item"},
            {"type": "Link", "label": "Bảng giá", "link_type": "DocType", "link_to": "Price List"},
        ],
    },
    {
        "label": "Kho VN",
        "title": "Kho VN",
        "icon": "package",
        "sequence_id": 73.0,
        "shortcuts": [
            {"label": "Kho", "type": "DocType", "link_to": "Warehouse", "doc_view": "Tree"},
            {"label": "Mặt hàng", "type": "DocType", "link_to": "Item", "doc_view": "List"},
            {"label": "Phiếu nhập xuất kho", "type": "DocType", "link_to": "Stock Entry", "doc_view": "List"},
            {"label": "Kiểm kê kho", "type": "DocType", "link_to": "Stock Reconciliation", "doc_view": "List"},
        ],
        "links": [
            {"type": "Card Break", "label": "Báo cáo kho"},
            {"type": "Link", "label": "Tồn kho", "link_type": "Report", "link_to": "Stock Balance"},
            {"type": "Link", "label": "Thẻ kho", "link_type": "Report", "link_to": "Stock Ledger"},
            {"type": "Link", "label": "Lô / Sê-ri", "link_type": "DocType", "link_to": "Serial and Batch Bundle"},
        ],
    },
]

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
