# toolshop-automation-group22

## Test case Sprint 1

| ID   | Chức năng | Các bước                                       | Dữ liệu                               | Kết quả mong đợi                                |
| ---- | --------- | ---------------------------------------------- | ------------------------------------- | ----------------------------------------------- |
| SM01 | Tìm kiếm  | Mở trang chủ, nhập từ khóa, tìm kiếm           | pliers                                | Có kết quả; mọi tên đều chứa pliers             |
| SM02 | Giỏ hàng  | Mở Claw Hammer, đặt số lượng 3, thêm vào giỏ   | Claw Hammer, 3                        | Toast thành công; badge bằng 3                  |
| SM03 | Đăng nhập | Nhập email không tồn tại và mật khẩu, gửi form | nobody-here@example.com, mật khẩu sai | Hiện lỗi; vẫn ở trang đăng nhập                 |
| SM04 | Liên hệ   | Mở Contact, để trống, gửi form                 | Biểu mẫu trống                        | Hiện Subject is required và Message is required |

## AI hỗ trợ

AI hỗ trợ giải thích Page Object Model và đề xuất nội dung smoke test.
Các thành viên tự áp dụng, chạy kiểm thử và chịu trách nhiệm giải thích code.
