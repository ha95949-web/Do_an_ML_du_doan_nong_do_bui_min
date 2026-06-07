#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Khởi tạo LCD 16x2 địa chỉ 0x27
LiquidCrystal_I2C lcd(0x27, 16, 2);

int ledPin = 7;       // Dây màu Xanh Lá điều khiển LED của cảm biến
int analogPin = A0;   // Dây màu Đen đọc tín hiệu Analog
int samplingTime = 280;
int deltaTime = 40;
int sleepTime = 9680;

float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;

void setup() {
  Serial.begin(9600); // Mở cổng Serial tốc độ 9600 baud
  pinMode(ledPin, OUTPUT);
  
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("He thong bui min");
  lcd.setCursor(0, 1);
  lcd.print("Dang khoi dong...");
  delay(2000);
  lcd.clear();
  
  // In sẵn tiêu đề cố định ở dòng 0 để màn hình không bị nhấp nháy
  lcd.setCursor(0, 0);
  lcd.print("Dust (mg/m3):");
}

void loop() {
  // Bước 1: Kích hoạt LED của cảm biến (Mức thấp LOW)
  digitalWrite(ledPin, LOW); 
  delayMicroseconds(samplingTime);
  
  // Bước 2: Đọc giá trị Analog từ chân A0
  voMeasured = analogRead(analogPin);
  
  delayMicroseconds(deltaTime);
  digitalWrite(ledPin, HIGH); // Tắt LED
  delayMicroseconds(sleepTime);

  // Bước 3: Chuyển đổi sang điện áp thực
  calcVoltage = voMeasured * (5.0 / 1023.0);
  
  // TÍNH TOÁN THEO PHƯƠNG TRÌNH AI (Đã lấy hệ số thực tế)
  dustDensity = 0.03982 * (calcVoltage * calcVoltage) + 0.02004 * calcVoltage - 0.04795;

  // Lọc nhiễu âm (Nếu không khí quá sạch, phương trình ra số âm thì ép về 0)
  if (dustDensity < 0) {
      dustDensity = 0.0000; 
  }

  // Bước 4: Hiển thị lên LCD 16x2 (Không dùng lcd.clear để tránh nhấp nháy)
  lcd.setCursor(0, 1);
  lcd.print(dustDensity, 4); // In ra 4 chữ số thập phân cho chính xác
  lcd.print("       ");      // Khoảng trắng để xóa các ký tự cũ thừa phía sau

  // Bước 5: Gửi dữ liệu định dạng CSV lên Serial (cho script Python đọc)
  // Định dạng đầu ra: Điện_áp,Mật_độ_bụi
  Serial.print(calcVoltage, 4);
  Serial.print(",");
  Serial.println(dustDensity, 4);
  
  delay(1000); // Đo lại sau mỗi 1 giây
}