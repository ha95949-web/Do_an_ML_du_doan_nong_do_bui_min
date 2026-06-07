Đồ Án Machine Learning - Robotics: Dự Báo Nồng Độ Bụi Mịn
•	Dự án xây dựng hệ thống đo lường nồng độ bụi mịn (mg/m3) thời gian thực bằng cách sử dụng cảm biến quang học Sharp GP2Y1010AU0F kết hợp vi điều khiển Arduino Uno R3 và mô hình Hồi quy Đa thức (Polynomial Regression) bậc 2 được huấn luyện trên môi trường Python.
•	 Tính Năng Hệ Thống
* Thu thập tín hiệu điện áp (Analog Voltage) từ cảm biến bụi Sharp thông qua bộ chuyển đổi ADC của Arduino.
* Áp dụng phương trình hồi quy đa thức bậc 2 đã được tối ưu hóa bằng Machine Learning để tự động hiệu chỉnh sai số vật lý và bù trừ nhiễu do môi trường.
* Hiển thị kết quả nồng độ bụi dự báo theo thời gian thực đồng bộ trên cả màn hình LCD 16x2 (phần cứng) và giao diện Terminal (máy tính).
•	 Yêu Cầu Cài Đặt (Prerequisites)
1. Thành phần phần cứng
* 1 x Board mạch điều khiển Arduino Uno R3
* 1 x Cảm biến bụi mịn Sharp GP2Y1010AU0F (kèm mạch lọc tụ và điện trở tiêu chuẩn)
* 1 x Màn hình LCD 16x2 tích hợp mô-đun chuyển đổi giao tiếp I2C
* Breadboard và dây cắm mạch
2. Môi trường phần mềm & Thư viện Python
-	Sử dụng phần mềm Arduino IDE sử dụng ngôn ngữ C++ viết kệnh để nạp vào bộ não bộ điều khiển là Arduino Uno
-	Phần mềm Visual Studio Code sử dụng ngôn ngữ Python để nhận tín hiệu đc truyền về từ cảm biến qua Arduino uno sau đó dựa vào dữ liệu thu thập đc dự đoán nồng độ bụi mịn và chạy mô hình ML 
-	Cài đặt các thư viện cần thiết phục vụ cho việc huấn luyện mô hình và giao tiếp nối tiếp (Serial) bằng lệnh sau:

```bash
pip install scikit-learn pandas numpy matplotlib pyserial


├── arduino_code/
│   └── src.ino          # Mã nguồn C++ nạp cho vi điều khiển Arduino Uno
├── python_ml/
│   ├── dataset.csv       # Tập dữ liệu mẫu (Điện áp - Nồng độ thực tế)
│   ├── main_robot.py   # Script Python huấn luyện mô hình Hồi quy Đa thức
│   └── run_realtime.py #Script Python nhận dữ liệu qua cổng Serial và dự báo
├── models/
│   └── model_poly.pkl   # File lưu trữ mô hình ML sau khi huấn luyện thành công
└── README.md            # File hướng dẫn này
