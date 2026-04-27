# Đơn Mua Hàng

Purchase Order là đơn đặt hàng gửi cho nhà cung cấp, DocType là Purchase Order.

Quy trình cơ bản:

1. Vào Purchase Order.
2. Chọn Supplier.
3. Thêm Item, số lượng và đơn giá thỏa thuận.
4. Kiểm tra ngày giao hàng dự kiến.
5. Save và Submit.

Sau khi submit:

- Dùng Make > Purchase Receipt để nhận hàng vào kho.
- Dùng Make > Purchase Invoice để tạo hóa đơn thanh toán.

Lấy từ Material Request:

- Nếu có yêu cầu mua hàng nội bộ, dùng Make từ Material Request để tạo Purchase Order tự động.

Lưu ý:

- Trạng thái To Receive: chờ nhận hàng. To Bill: chờ hóa đơn.
- Có thể nhận hàng nhiều lần (partial receipt) trước khi đủ số lượng.
