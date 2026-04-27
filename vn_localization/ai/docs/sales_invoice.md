# Hóa Đơn Bán Hàng

Hóa đơn bán hàng trong ERPNext thường nằm ở Selling hoặc Accounting, DocType là Sales Invoice.

Quy trình cơ bản:

1. Vào Sales Invoice.
2. Chọn Customer.
3. Thêm Item, số lượng, đơn giá và thuế nếu có.
4. Kiểm tra ngày hạch toán, kho, tài khoản thuế và tổng tiền.
5. Save.
6. Submit nếu thông tin đã đúng.

Lưu ý:

- Nếu hóa đơn lấy từ Sales Order hoặc Delivery Note, nên dùng chức năng Make để ERPNext tự kéo dữ liệu.
- Nếu cần ghi nhận thanh toán ngay, kiểm tra phần Payment hoặc tạo Payment Entry sau khi submit.
- Với VAT, chọn đúng Sales Taxes and Charges Template.

