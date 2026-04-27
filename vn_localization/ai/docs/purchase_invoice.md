# Hóa Đơn Mua Hàng

Hóa đơn mua hàng ghi nhận công nợ phải trả cho nhà cung cấp, DocType là Purchase Invoice.

Quy trình cơ bản:

1. Vào Purchase Invoice.
2. Chọn Supplier.
3. Thêm Item, số lượng, đơn giá và thuế nếu có.
4. Chọn đúng kho nhận hàng nếu có cập nhật tồn kho.
5. Save và Submit.

Lấy từ Purchase Order hoặc Purchase Receipt:

- Dùng chức năng Make từ Purchase Order hoặc Purchase Receipt để ERPNext tự kéo dữ liệu.
- Giúp tránh nhập liệu trùng và đảm bảo đối chiếu đúng.

Lưu ý:

- Nếu hóa đơn không cập nhật tồn kho, bỏ tích Update Stock.
- Kiểm tra Purchase Taxes and Charges Template cho đúng thuế đầu vào.
- Sau khi submit, tạo Payment Entry để thanh toán cho nhà cung cấp.
