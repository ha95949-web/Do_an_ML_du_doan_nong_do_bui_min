import pickle
import numpy as np
import serial
import time

# =====================================================================
# 1. CẤU HÌNH CỔNG GIAO TIẾP VỚI ARDUINO
# =====================================================================
# Sửa 'COM3' thành cổng COM thực tế mà bạn đang cắm Arduino
COM_PORT = 'COM5' 
BAUD_RATE = 9600

# =====================================================================
# 2. TẢI "BỘ NÃO" AI ĐÃ HUẤN LUYỆN
# =====================================================================
try:
    with open('model_buimin.pkl', 'rb') as file:
        poly_features, model = pickle.load(file)
    print("[*] Đã tải mô hình AI thành công!")
except FileNotFoundError:
    print("[LỖI] Không tìm thấy file 'model_buimin.pkl'. Hãy chạy file main_robot.py trước!")
    exit()

# =====================================================================
# 3. KẾT NỐI VỚI ARDUINO
# =====================================================================
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    print(f"[*] Đã kết nối thành công với mạch tại cổng {COM_PORT}")
    time.sleep(2) # Chờ 2 giây để mạch Arduino ổn định sau khi mở cổng
except Exception as e:
    print(f"[LỖI] Không thể mở cổng {COM_PORT}.")
    print("-> Gợi ý: Bạn đã cắm cáp chưa? Hoặc có quên TẮT màn hình Serial Monitor bên Arduino IDE không?")
    exit()

# =====================================================================
# 4. HÀM PHÂN LOẠI CHẤT LƯỢNG KHÔNG KHÍ (Theo chuẩn AQI)
# =====================================================================
def danh_gia_chat_luong(mat_do_mg_m3):
    mat_do_ug = mat_do_mg_m3 * 1000 
    
    if mat_do_ug <= 12.0:
        return "🟢 TỐT (Không khí trong lành)"
    elif mat_do_ug <= 35.4:
        return "🟡 TRUNG BÌNH (Chấp nhận được)"
    elif mat_do_ug <= 55.4:
        return "🟠 KÉM (Nhạy cảm với người già, trẻ em)"
    elif mat_do_ug <= 150.4:
        return "🔴 XẤU (Ô nhiễm, có hại cho sức khỏe)"
    else:
        return "🟣 RẤT XẤU (Báo động nguy hiểm!)"

# =====================================================================
# 5. VÒNG LẶP ĐỌC DỮ LIỆU VÀ DỰ BÁO THỜI GIAN THỰC
# =====================================================================
print("\n" + "=" * 75)
print(f"{'ĐIỆN ÁP (V)':<15} | {'MẬT ĐỘ BỤI (mg/m3)':<20} | {'CẢNH BÁO CHẤT LƯỢNG KHÔNG KHÍ'}")
print("=" * 75)

while True:
    try:
        # Kiểm tra xem Arduino có đang gửi dữ liệu lên không
        if ser.in_waiting > 0:
            # Đọc 1 dòng dữ liệu từ Arduino, giải mã và xóa khoảng trắng thừa
            data_str = ser.readline().decode('utf-8').strip()
            
            # Tách lấy giá trị điện áp (phòng trường hợp Arduino gửi kèm nhiều thông số khác cách nhau bởi dấu phẩy)
            parts = data_str.split(',')
            if len(parts) >= 1:
                dien_ap_doc_ve = float(parts[0])

                # Đưa điện áp vào định dạng ma trận để AI đọc được
                X_input = np.array([[dien_ap_doc_ve]])
                X_input_poly = poly_features.transform(X_input)

                # AI Bắt đầu dự báo
                nong_do_du_bao = model.predict(X_input_poly)[0]
                
                # Ép giá trị về 0 nếu bị âm do nhiễu dải dưới
                nong_do_du_bao = max(0, nong_do_du_bao)

                # Gọi hàm đánh giá
                canh_bao = danh_gia_chat_luong(nong_do_du_bao)

                # In ra Bảng điều khiển (Dashboard)
                print(f"⚡ {dien_ap_doc_ve:<12.2f} | 🌫️ {nong_do_du_bao:<17.4f} | {canh_bao}")
                
    except ValueError:
        # Bỏ qua nếu dòng đọc lên bị lỗi font hoặc bị mất gói tin giật cục
        pass
    except KeyboardInterrupt:
        # Khi bạn bấm Ctrl + C để thoát chương trình
        print("\n[*] Đã đóng cổng COM. Dừng hệ thống giám sát.")
        ser.close()
        break
    except Exception as e:
        print(f"\n[LỖI KHÔNG XÁC ĐỊNH]: {e}")
        ser.close()
        break