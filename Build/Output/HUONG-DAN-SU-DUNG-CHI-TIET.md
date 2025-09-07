# XML GUARD ENTERPRISE - HƯỚNG DẪN SỬ DỤNG CHI TIẾT

## 🎯 TỔNG QUAN
**XML Guard Enterprise** là hệ thống bảo vệ file XML tự động, tích hợp với MeshCentral để quản lý tập trung nhiều doanh nghiệp.

## 📦 PACKAGE CHO DOANH NGHIỆP

### 1.1 NỘI DUNG PACKAGE
```
📁 XML-Guard-Enterprise-Package/
├── 🚀 Setup-Enterprise.bat          # File chính - chạy 1 lần
├── 🤖 XML-Guard-Optimized.exe       # Main executable (32MB)
├── 📋 README-ENTERPRISE.md          # Hướng dẫn
├── 📁 Core/                         # Core modules
├── 📁 Utils/                        # Utilities
├── 📁 Config/                       # Configuration
└── 📁 Logs/                         # Log files
```

### 1.2 CÁCH GỬI PACKAGE

#### **Phương án 1: Gửi qua Zalo/Email**
1. **Nén toàn bộ thư mục** `Build/Output/` thành file ZIP
2. **Đặt tên:** `XML-Guard-Enterprise-v2.0.zip`
3. **Gửi qua Zalo/Email** cho doanh nghiệp
4. **Hướng dẫn:** "Giải nén và chạy `Setup-Enterprise.bat`"

#### **Phương án 2: Upload lên MeshCentral**
1. **Vào MeshCentral** → https://103.69.86.130:4433
2. **Tạo thư mục** "XML-Guard-Package"
3. **Upload file ZIP** lên thư mục này
4. **Gửi link download** cho doanh nghiệp

#### **Phương án 3: Tạo link download**
1. **Upload lên Google Drive/OneDrive**
2. **Tạo link chia sẻ**
3. **Gửi link** cho doanh nghiệp

## 🏢 HƯỚNG DẪN CHO DOANH NGHIỆP

### 2.1 CÀI ĐẶT LẦN ĐẦU

#### **Bước 1: Tải Package**
- Tải file `XML-Guard-Enterprise-v2.0.zip`
- Giải nén vào thư mục bất kỳ (ví dụ: `C:\XML-Guard\`)

#### **Bước 2: Chạy Setup**
```bash
# Mở thư mục đã giải nén
cd C:\XML-Guard\

# Chạy setup tự động
Setup-Enterprise.bat
```

#### **Bước 3: Kiểm tra**
- Setup sẽ tự động:
  - ✅ Kiểm tra Python
  - ✅ Cài đặt dependencies
  - ✅ Build EXE
  - ✅ Test hệ thống
  - ✅ Tạo shortcuts

### 2.2 SỬ DỤNG HÀNG NGÀY

#### **Khởi động:**
```bash
# Cách 1: Click shortcut trên Desktop
XML-Guard-Enterprise.lnk

# Cách 2: Chạy trực tiếp
XML-Guard-Optimized.exe start
```

#### **Dừng:**
```bash
XML-Guard-Optimized.exe stop
```

#### **Kiểm tra trạng thái:**
```bash
XML-Guard-Optimized.exe status
```

#### **Test hệ thống:**
```bash
XML-Guard-Optimized.exe test
```

## 🔄 WORKFLOW TỰ ĐỘNG

### 3.1 HOẠT ĐỘNG TỰ ĐỘNG
1. **Khởi động** → Tự động kết nối MeshCentral
2. **Monitor** → Tự động theo dõi file XML
3. **Phân loại** → Tự động phân loại bằng AI
4. **Upload** → Tự động upload lên MeshCentral
5. **Download** → Tự động download updates
6. **Restart** → Tự động restart nếu cần

### 3.2 KHÔNG CẦN CAN THIỆP
- ✅ **Tự động chạy** khi khởi động máy
- ✅ **Tự động kết nối** MeshCentral
- ✅ **Tự động bảo vệ** file XML
- ✅ **Tự động update** khi có XML mới
- ✅ **Tự động restart** nếu có lỗi

## 🎛️ QUẢN LÝ TẬP TRUNG (CHO ANH)

### 4.1 UPLOAD XML MỚI
1. **Vào MeshCentral** → https://103.69.86.130:4433
2. **Tạo thư mục** "XML-Templates" (nếu chưa có)
3. **Upload file XML** mới vào thư mục này
4. **Tất cả agents** sẽ tự động download

### 4.2 MONITOR DOANH NGHIỆP
1. **Vào MeshCentral** → Dashboard
2. **Xem danh sách** agents đang kết nối
3. **Kiểm tra trạng thái** từng doanh nghiệp
4. **Xem logs** hoạt động

### 4.3 QUẢN LÝ NGƯỜI DÙNG
1. **Tạo tài khoản** cho từng doanh nghiệp
2. **Phân quyền** truy cập
3. **Gửi thông tin** đăng nhập
4. **Hỗ trợ** khi cần thiết

## 📊 MONITORING & BÁO CÁO

### 5.1 DASHBOARD MESHCENTRAL
- **Tổng số agents:** Hiển thị số lượng
- **Trạng thái kết nối:** Online/Offline
- **Memory usage:** 32MB per agent
- **Network status:** Ping time
- **Last update:** Thời gian cập nhật cuối

### 5.2 LOGS & BÁO CÁO
- **Logs tự động** lưu trong thư mục `Logs/`
- **Báo cáo hàng ngày** gửi qua email
- **Alert** khi có lỗi xảy ra
- **Performance metrics** real-time

## 🔧 TROUBLESHOOTING

### 6.1 LỖI THƯỜNG GẶP

#### **Lỗi kết nối MeshCentral:**
```bash
# Kiểm tra internet
ping google.com

# Kiểm tra MeshCentral
ping 103.69.86.130

# Restart agent
XML-Guard-Optimized.exe stop
XML-Guard-Optimized.exe start
```

#### **Lỗi memory cao:**
```bash
# Restart agent
XML-Guard-Optimized.exe stop
XML-Guard-Optimized.exe start

# Kiểm tra memory
XML-Guard-Optimized.exe test
```

#### **Lỗi file XML:**
```bash
# Kiểm tra thư mục Core
dir Core

# Kiểm tra logs
type Logs\xmlguard.log
```

### 6.2 HỖ TRỢ KHÁCH HÀNG
1. **Gửi hướng dẫn** troubleshooting
2. **Remote support** qua MeshCentral
3. **Update package** khi cần
4. **Training** sử dụng

## 🎯 KẾT QUẢ MONG MUỐN

### ✅ CHO ANH (ADMIN):
- **1 lần setup** MeshCentral server
- **1 lần build** package
- **Quản lý tập trung** tất cả doanh nghiệp
- **Update 1 lần** → áp dụng cho tất cả
- **Monitor real-time** tất cả agents

### ✅ CHO DOANH NGHIỆP:
- **Cài đặt 1 lần** → Setup-Enterprise.bat
- **Tự động hoạt động** → Không cần can thiệp
- **Tự động update** → XML mới từ server
- **Bảo vệ tự động** → File XML
- **Báo cáo tự động** → Lên server

## 📞 LIÊN HỆ HỖ TRỢ

### **Khi cần hỗ trợ:**
1. **Gửi email** với thông tin lỗi
2. **Gửi logs** từ thư mục `Logs/`
3. **Mô tả** vấn đề gặp phải
4. **Chụp màn hình** nếu cần

### **Thông tin cần cung cấp:**
- Tên doanh nghiệp
- Phiên bản package
- Lỗi gặp phải
- Logs chi tiết
- Thời gian xảy ra lỗi

---

**XML Guard Enterprise - Bảo vệ XML tự động, quản lý tập trung!** 🛡️✨
