# Đơn Bán Hàng

Sales Order xác nhận đơn hàng từ khách hàng, DocType là Sales Order.

Quy trình cơ bản:

1. Vào Sales Order.
2. Chọn Customer.
3. Thêm Item, số lượng và đơn giá.
4. Kiểm tra ngày giao hàng.
5. Save và Submit.

Sau khi submit:

- Dùng Make > Delivery Note để tạo phiếu giao hàng.
- Dùng Make > Sales Invoice để tạo hóa đơn bán hàng.

Lấy từ Quotation:

- Nếu đã có báo giá, dùng Make từ Quotation để tạo Sales Order tự động.

Lưu ý:

- Trạng thái To Deliver: chờ giao hàng. To Bill: chờ lập hóa đơn.
- Có thể giao hàng nhiều lần (partial delivery) trước khi đủ số lượng.
- Kiểm tra tồn kho trước khi commit đơn hàng lớn.
