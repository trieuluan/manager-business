# Phiếu Nhập Kho

Purchase Receipt ghi nhận việc nhận hàng từ nhà cung cấp vào kho, DocType là Purchase Receipt.

Quy trình cơ bản:

1. Từ Purchase Order đã submit, dùng Make > Purchase Receipt.
2. Kiểm tra Item, số lượng thực nhận và kho nhận.
3. Save và Submit.

Hoặc tạo trực tiếp:

1. Vào Purchase Receipt.
2. Chọn Supplier.
3. Thêm Item, số lượng và kho nhận hàng.
4. Save và Submit.

Sau khi submit:

- Tồn kho tự động tăng theo số lượng nhận.
- Dùng Make > Purchase Invoice để tạo hóa đơn mua hàng.

Lưu ý:

- Có thể nhận hàng nhiều lần cho cùng một Purchase Order (partial receipt).
- Nếu trả hàng, tạo Purchase Return từ Purchase Receipt gốc.
- Kiểm tra đúng kho nhận để tồn kho cập nhật đúng vị trí.
