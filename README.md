
⚙️ Tool Upload Truyện Hàng Loạt
Một công cụ có giao diện đồ họa (GUI) được viết bằng Python, giúp tự động hóa việc đăng tải hàng loạt chương truyện tranh/tiểu thuyết lên các trang web, tiết kiệm tối đa thời gian và công sức.
(Ghi chú: Bạn nên chụp ảnh màn hình ứng dụng của mình và thay thế link ảnh này)
✨ Tính năng chính
 * Đăng Hàng Loạt: Dễ dàng đăng tải một khoảng chương truyện (ví dụ: từ chương 1 đến 100) chỉ với một lần thiết lập.
 * Giao Diện Trực Quan: Toàn bộ chức năng được gói gọn trong một cửa sổ ứng dụng đơn giản, không cần kiến thức về lập trình.
 * Tự Động Hoàn Toàn:
   * Tự động quản lý Driver: Tự động kiểm tra phiên bản Chrome và tải về chromedriver tương ứng. Không cần người dùng cài đặt thủ công.
   * Tự động cài đặt thư viện: Tự động cài đặt Selenium và webdriver-manager nếu máy tính chưa có.
   * Tự động nhận diện link: Chỉ cần dán link của trang "Thêm chương mới", tool sẽ tự suy ra link đăng nhập.
 * Tìm Kiếm Thư Mục Thông Minh: Linh hoạt nhận diện các thư mục chương với nhiều kiểu đặt tên khác nhau (Chapter-101, chuong 101, chap101, 101, v.v...).
⚙️ Yêu cầu
 * Hệ điều hành: Windows.
 * Trình duyệt: Google Chrome đã được cài đặt.
 * Python 3.x (chỉ cần thiết nếu bạn chạy trực tiếp từ mã nguồn .py).
🚀 Hướng dẫn cài đặt và sử dụng
### Dành cho người dùng thông thường (sử dụng file .EXE)
Cách đơn giản nhất để sử dụng tool mà không cần cài đặt gì phức tạp.
 * Truy cập vào mục "Releases" của dự án trên GitHub.
 * Tải về file .zip của phiên bản mới nhất.
 * Giải nén file .zip ra một thư mục bất kỳ.
 * Chạy file .exe bên trong thư mục vừa giải nén để khởi động ứng dụng.
### Dành cho Lập trình viên (chạy từ mã nguồn .py)
 * Clone lại dự án này từ GitHub.
 * Mở Command Prompt (cmd) trong thư mục dự án.
 * Chạy lệnh:
   python toolupload.py

 * Lần đầu tiên chạy, tool sẽ tự động kiểm tra và cài đặt các thư viện cần thiết (selenium, webdriver-manager). Sau khi cài đặt xong, bạn chỉ cần chạy lại lệnh trên một lần nữa.
📝 Hướng dẫn sử dụng Giao diện
 * Thông tin đăng nhập: Điền tài khoản và mật khẩu của bạn.
 * Link Đăng Chương Mới: Dán link trực tiếp đến trang thêm chương mới của bộ truyện bạn muốn đăng.
 * Thư mục gốc chứa chương: Nhấn nút "Chọn Thư Mục Gốc" và trỏ đến thư mục lớn chứa các thư mục con của từng chương (ví dụ: D:/TruyenA).
 * Đăng từ chương số / Đến chương số: Nhập khoảng chương bạn muốn đăng.
 * Nhấn nút "BẮT ĐẦU ĐĂNG HÀNG LOẠT" và để tool tự làm việc.
🛠️ Đóng gói thành file .EXE (Tùy chọn)
Nếu bạn muốn tự đóng gói lại file .exe từ mã nguồn, hãy làm theo các bước sau:
 * Cài đặt PyInstaller:
   pip install pyinstaller

 * Mở cmd trong thư mục chứa file .py, chạy lệnh:
   pyinstaller --onefile --windowed ten_file_tool.py

 * File .exe hoàn chỉnh sẽ nằm trong thư mục dist mới được tạo ra.
❤️ Tác giả & Ủng hộ
Tool được làm ra với tâm huyết để giúp đỡ cộng đồng. Nếu nó hữu ích, bạn có thể ủng hộ tác giả một ly cafe!
 * Credit: odaycoduong
 * Donate MB bank: 0345279983
