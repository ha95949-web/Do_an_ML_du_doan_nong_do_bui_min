import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os
import pickle

# =====================================================================
# PHẦN 1: KHỞI TẠO HOẶC ĐỌC DATASET THỰC NGHIỆM
# =====================================================================
if not os.path.exists('dataset_buimin.csv'):
    print("[*] Không thấy file dữ liệu cũ, tự động khởi tạo dataset thực nghiệm mới...")
    np.random.seed(42)
    dien_ap = np.random.uniform(1.2, 3.5, 600)  
    
    # CÔNG THỨC MỚI: Sử dụng phương trình bậc 2 để tạo đặc tính cong thực tế cho cảm biến
    mat_do_bui = 0.04 * (dien_ap ** 2) + 0.02 * dien_ap - 0.05 + np.random.normal(0, 0.015, 600)
    mat_do_bui = np.clip(mat_do_bui, 0, None) 

    df_generated = pd.DataFrame({'Dien_Ap_V': dien_ap, 'Mat_Do_Bui_mg_m3': mat_do_bui})
    df_generated.to_csv('dataset_buimin.csv', index=False)
    print("[*] Đã tạo thành công file 'dataset_buimin.csv' với dữ liệu phi tuyến tính!\n")

df = pd.read_csv('dataset_buimin.csv')
print("[*] Đọc dữ liệu thành công! Số lượng mẫu huấn luyện:", len(df))

# =====================================================================
# PHẦN 2: CHUẨN BỊ VÀ CHIA TẬP DỮ LIỆU (TRAIN / TEST)
# =====================================================================
X = df[['Dien_Ap_V']].values
y = df['Mat_Do_Bui_mg_m3'].values

# Phân bổ 80% dữ liệu để AI học (Train) và 20% để làm bài kiểm tra (Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# =====================================================================
# PHẦN 3: KHỞI TẠO, HUẤN LUYỆN VÀ LƯU MÔ HÌNH MACHINE LEARNING
# =====================================================================
# 3.1 Cấu hình thuật toán Hồi quy đa thức bậc 2
poly_features = PolynomialFeatures(degree=2)
X_train_poly = poly_features.fit_transform(X_train)
X_test_poly = poly_features.transform(X_test)

# 3.2 Cho mô hình học trên dữ liệu
model = LinearRegression()
model.fit(X_train_poly, y_train)
print("[*] Huấn luyện mô hình Hồi quy Đa thức thành công!")

# 3.3 Lưu bộ não AI ra file .pkl để triển khai thực tế sau này
with open('model_buimin.pkl', 'wb') as file:
    pickle.dump((poly_features, model), file)
print("[*] Đã đóng gói và lưu mô hình vào file 'model_buimin.pkl'")

# =====================================================================
# PHẦN 4: DỰ ĐOÁN VÀ ĐÁNH GIÁ ĐỘ CHÍNH XÁC CỦA MÔ HÌNH
# =====================================================================
# Cho AI làm bài thi trên 20% tập Test
y_pred = model.predict(X_test_poly)

# Chấm điểm sai số
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n" + "="*30 + " KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH " + "="*30)
print(f"- Sai số tuyệt đối trung bình (MAE): {mae:.5f} mg/m3")
print(f"- Căn sai số bình phương trung bình (RMSE): {rmse:.5f} mg/m3")
print(f"- Độ chính xác mô hình (R2 Score): {r2*100:.2f}%")
print("="*85)

# =====================================================================
# PHẦN 5: VẼ ĐỒ THỊ SO SÁNH VÀ ĐÁNH GIÁ ĐỂ ĐƯA VÀO BÁO CÁO
# =====================================================================
# Khởi tạo Lưới dữ liệu mượt mà để vẽ đường cong
X_grid = np.arange(X.min(), X.max(), 0.01).reshape(-1, 1)

# --- ĐỒ THỊ 1: SO SÁNH TUYẾN TÍNH (LINEAR) VÀ ĐA THỨC (POLYNOMIAL) ---
# Huấn luyện nhanh một mô hình Tuyến tính thuần túy để làm đối chứng
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

plt.figure(figsize=(10, 6))
# Quần thể dữ liệu thực
plt.scatter(X, y, color='lightgray', alpha=0.7, label='Dữ liệu thực tế (Cảm biến đo)')

# Đường Tuyến tính (Linear)
plt.plot(X_grid, linear_model.predict(X_grid), color='blue', linestyle='--', linewidth=2, label='Mô hình Tuyến tính (Linear)')

# Đường Đa thức bậc 2 (Polynomial)
X_grid_poly = poly_features.transform(X_grid)
plt.plot(X_grid, model.predict(X_grid_poly), color='red', linewidth=3, label='Mô hình Đa thức bậc 2 (Polynomial)')

plt.title('SO SÁNH MÔ HÌNH: TUYẾN TÍNH VÀ ĐA THỨC BẬC 2', fontsize=14, fontweight='bold')
plt.xlabel('Điện áp đọc về (V)', fontsize=12)
plt.ylabel('Mật độ bụi mịn (mg/m3)', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':')
plt.savefig('dothi_1_sosanh_thuattoan.png', dpi=300, bbox_inches='tight')
print("\n[*] Đã lưu Đồ thị 1: 'dothi_1_sosanh_thuattoan.png'")


# --- ĐỒ THỊ 2: THỰC TẾ VS. DỰ BÁO (ACTUAL VS PREDICTED) ---
plt.figure(figsize=(8, 8)) 

# Các điểm Test
plt.scatter(y_test, y_pred, color='green', alpha=0.6, edgecolors='black', label='Điểm dữ liệu Test')

# Đường chéo lý tưởng
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', linewidth=2, label='Đường lý tưởng (Sai số = 0)')

plt.title('ĐÁNH GIÁ ĐỘ LỆCH: THỰC TẾ VÀ DỰ BÁO', fontsize=14, fontweight='bold')
plt.xlabel('Nồng độ bụi thực tế (mg/m3)', fontsize=12)
plt.ylabel('Nồng độ bụi AI dự báo (mg/m3)', fontsize=12)
plt.legend()
plt.grid(True, linestyle=':')
plt.savefig('dothi_2_thucte_vs_dubao.png', dpi=300, bbox_inches='tight')
print("[*] Đã lưu Đồ thị 2: 'dothi_2_thucte_vs_dubao.png'")

# Hiển thị tất cả đồ thị lên màn hình
plt.show()