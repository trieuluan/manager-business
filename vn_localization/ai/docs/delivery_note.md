# Phiếu Giao Hàng

Delivery Note ghi nhận việc xuất hàng giao cho khách hàng, DocType là Delivery Note.

Quy trình cơ bản:

1. Từ Sales Order đã submit, dùng Make > Delivery Note.
2. Kiểm tra Item, số lượng, kho xuất hàng.
3. Save và Submit.

Hoặc tạo trực tiếp:

1. Vào Delivery Note.
2. Chọn Customer.
3. Thêm Item, số lượng và kho xuất.
4. Save và Submit.

Sau khi submit:

- Tồn kho tự động giảm theo số lượng giao.
- Dùng Make > Sales Invoice để lập hóa đơn nếu chưa có.

Lưu ý:

- Có thể giao hàng nhiều lần cho cùng một Sales Order (partial delivery).
- Nếu trả hàng, tạo Sales Return từ Delivery Note gốc.
- Kiểm tra tồn kho đủ trước khi submit để tránh lỗi âm kho.
