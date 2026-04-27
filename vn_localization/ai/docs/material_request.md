# Yêu Cầu Mua Hàng

Material Request là phiếu yêu cầu mua hàng hoặc cấp vật tư nội bộ, DocType là Material Request.

Các loại yêu cầu:

- Purchase: yêu cầu mua hàng từ nhà cung cấp.
- Material Transfer: yêu cầu chuyển vật tư từ kho khác.
- Material Issue: yêu cầu xuất vật tư từ kho.
- Manufacture: yêu cầu sản xuất.

Quy trình mua hàng:

1. Vào Material Request.
2. Chọn Material Request Type là Purchase.
3. Thêm Item và số lượng cần mua.
4. Save và Submit.
5. Dùng Make > Purchase Order để tạo đơn mua hàng.

Lưu ý:

- Có thể tạo tự động từ reorder level khi tồn kho xuống thấp.
- Một Material Request có thể tạo nhiều Purchase Order cho nhiều nhà cung cấp.
- Kiểm tra trạng thái Pending, Ordered, Received để theo dõi tiến độ.
