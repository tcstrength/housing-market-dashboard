# Housing Market Dashboard

## Nguồn khai thác
Có nhiều nguồn mà nhóm muốn khai thác, trong đó bao gồm cafef.vn, batdongsan.com, nhatot.com, cenhomes.vn, trong đó nhóm nhận thấy nguồn từ chợ tốt sẽ thường có các trường thông tin cố định so với batdongsan.com thì các trường thông tin không cố định. Đối với cafef.vn chủ yếu là thông tin thị trường hơn là các thông tin chi tiết về nhà ở, cenhomes.vn yêu cầu đăng nhập và không tiện trong việc khai thác.

Dựa vào các thông tin trên, nhóm chọn khai thác ở nguồn nhatot.vn.

## Xác định một đối tượng
Việc xác định thế nào là một đối tượng là cần thiết, vì chúng ta sẽ cần cập nhật thông tin hoặc loại những đối tượng đã lưu vào cơ sở dữ liệu. May mắn, nhóm nhận thấy trên thanh địa chỉ, ID của đối tượng được dùng để truy cập các thông tin của đối tượng, ví dụ:

- https://www.nhatot.com/mua-ban-can-ho-chung-cu-thanh-pho-thuan-an-binh-duong/120304853.htm#px=SR-stickyad-[PO-2][PL-top]
- https://www.nhatot.com/mua-ban-can-ho-chung-cu-huyen-binh-chanh-tp-ho-chi-minh/111706207.htm#px=SR-stickyad-[PO-1][PL-top]

Chúng ta thấy URL có định dạng như sau:
- https://www.nhatot.com/<summary>/ID
- Nhóm có thử thay copy ID và thay đổi phần summary thì cho thấy phần summary chỉ là phụ và làm đẹp cho URL
- https://www.nhatot.com/khong-quan-trong/120304853.htm sẽ được redirect về https://www.nhatot.com/mua-ban-can-ho-chung-cu-thanh-pho-thuan-an-binh-duong/120304853.htm#px=SR-stickyad-[PO-2][PL-top]

