# Báo Giá

Quotation dùng để gửi báo giá cho khách hàng trước khi xác nhận đơn hàng, DocType là Quotation.

Quy trình cơ bản:

1. Vào Quotation.
2. Chọn Quotation To là Customer hoặc Lead.
3. Chọn Customer hoặc Lead.
4. Thêm Item, số lượng và đơn giá.
5. Save và Submit.
6. Gửi báo giá cho khách qua email hoặc in PDF.

Chuyển thành đơn hàng:

- Khi khách xác nhận, dùng Make > Sales Order từ Quotation.
- ERPNext tự kéo toàn bộ thông tin sang Sales Order.

Lưu ý:

- Có thể tạo nhiều phiên bản báo giá cho cùng khách hàng.
- Trạng thái Open: chờ phản hồi. Ordered: đã chuyển thành đơn hàng. Lost: khách từ chối.
- Ghi lý do mất đơn vào Lost Reason để theo dõi.
