# Surface-Intergral
Đây là công cụ phần mềm mã nguồn mở được phát triển phục vụ trực tiếp cho công việc tính toán nhanh chóng các phương trình tích phân mặt.

Phần mềm được xây dựng để số hóa và trực quan hóa các phương pháp giải tích, mục tiêu chính là hỗ trợ tính toán tự động, kiểm chứng kết quả lý thuyết và cung cấp hình ảnh không gian 3D trực quan cho các bài toán thường gặp trong chương trình học.

# Các tính năng nổi bật:

## Giải quyết các dạng tích phân mặt:
Hỗ trợ thiết lập và giải quyết bài toán tính diện tích mặt cong, tích phân mặt loại 1 (hàm vô hướng) và tích phân mặt loại 2 (thông lượng của trường vector qua mặt cong), là những nội dung cốt lõi để phát triển các ứng dụng vật lý như tính khối lượng, tọa độ trọng tâm, hay thông lượng chất lỏng.

## Mô hình hóa toán học linh hoạt:
Cho phép người dùng chuyển đổi linh hoạt giữa các mặt cong cơ bản (Mặt cầu, Paraboloid, Nón, Trụ) hoặc tự định nghĩa mặt cong $S$ thông qua phương trình tham số $R(u,v)$ và phương trình Descartes.

## Đối chiếu kết quả Đa phương pháp:
Hệ thống xử lý song song hai hướng giải: 
- dùng SciPy để xấp xỉ giá trị số phân tích nhanh;
- dùng SymPy để giữ nguyên tính chính xác tuyệt đối của công thức tích phân nguyên bản.

## Trực quan hóa không gian 3D:
Biểu diễn trực tiếp mặt cong $S$ cùng hệ trục tọa độ Oxyz thông qua thư viện Matplotlib, giúp người học dễ dàng hình dung miền lấy tích phân, từ đó hỗ trợ việc xác định pháp tuyến và cận tích phân chuẩn xác hơn.

# Thư viện và Ngôn ngữ lập trình đã dùng:
- Ngôn ngữ lập trình: Python
- Thư viện:
  - Xử lý toán học: SymPy, SciPy, NumPy.
  - Giaodieen và đồ họa: CustomTkinter, Matplotlib.
# Hình ảnh của ứng dụng:
<img width="1919" height="1007" alt="Ứng dụng tính toán tích phân mặt" src="https://github.com/user-attachments/assets/eada5ab1-3a65-42a4-ae9c-d8eb43b756fe" />
