# 🚀 XML GUARD ENTERPRISE - ADMIN QUICK START GUIDE

## 🎯 TÓM TẮT NHANH:

Bạn có **VPS với MeshCentral** và muốn tạo package **1-click EXE** cho khách hàng. Đây là hướng dẫn nhanh:

## 📦 CÁCH BUILD PACKAGE:

### Bước 1: Build package
```powershell
# Chạy script build (trên Windows)
cd Build
.\Build-All-Packages.ps1 -Version "2.0.0" -MeshCentralUrl "https://103.69.86.130:4433"
```

### Bước 2: Lấy package
- **File ZIP**: `Build\XML-Guard-Enterprise-v2.0.0.zip`
- **Gửi cho khách hàng**: Upload lên MeshCentral hoặc Google Drive

## 🎯 CÁCH GỬI CHO KHÁCH HÀNG:

### Phương án 1: MeshCentral (Khuyến nghị)
1. **Vào MeshCentral**: https://103.69.86.130:4433
2. **Upload ZIP** lên Files
3. **Tạo link download** cho khách hàng
4. **Gửi link** qua Zalo/Email

### Phương án 2: Google Drive
1. **Upload ZIP** lên Google Drive
2. **Tạo link chia sẻ** (Anyone with link can view)
3. **Gửi link** cho khách hàng

### Phương án 3: Zalo/Email
1. **Gửi file ZIP** trực tiếp
2. **Hướng dẫn**: Giải nén và chạy `XML-Guard-Enterprise.bat`

## 👥 HƯỚNG DẪN CHO KHÁCH HÀNG:

### Khách hàng cần làm:
1. **Tải file ZIP** từ link bạn gửi
2. **Giải nén** vào thư mục bất kỳ
3. **Cài đặt Python** (nếu chưa có): https://python.org
4. **Right-click** vào `XML-Guard-Enterprise.bat`
5. **Chọn "Run as administrator"**
6. **Xong!** Hệ thống tự động bảo vệ XML

## 📊 QUẢN LÝ KHÁCH HÀNG:

### Monitor qua MeshCentral:
1. **Vào MeshCentral**: https://103.69.86.130:4433
2. **Xem danh sách agents** đã kết nối
3. **Monitor real-time** hoạt động
4. **Upload XML mới** cho tất cả khách hàng

### Upload XML mới:
1. **Vào MeshCentral** → Files
2. **Upload XML mới** lên server
3. **Tất cả agents** tự động download
4. **Không cần can thiệp** thêm

## 🔧 TROUBLESHOOTING:

### Nếu khách hàng gặp lỗi:

#### Lỗi "Python not found":
- **Giải pháp**: Cài đặt Python từ https://python.org
- **Hướng dẫn**: Check "Add Python to PATH" during installation

#### Lỗi "Access denied":
- **Giải pháp**: Right-click → "Run as administrator"

#### Lỗi kết nối mạng:
- **Kiểm tra**: Firewall/Antivirus
- **Kiểm tra**: Kết nối internet
- **Kiểm tra**: Server MeshCentral

### Logs để debug:
- **File**: `xmlguard.log` (trong thư mục khách hàng)
- **Chứa**: Thông tin chi tiết về lỗi
- **Gửi cho admin**: Khi cần hỗ trợ

## 📈 SCALING CHO NHIỀU KHÁCH HÀNG:

### Workflow:
1. **1 lần build** package này
2. **Gửi cho tất cả** khách hàng
3. **Quản lý tập trung** qua MeshCentral
4. **Update 1 lần** → áp dụng cho tất cả

### Lợi ích:
- ✅ **Không cần cài đặt** gì thêm (trừ Python)
- ✅ **Không cần biết công nghệ**
- ✅ **Chỉ cần 1 click** là xong
- ✅ **Quản lý tập trung** dễ dàng

## 🎯 KẾT QUẢ MONG MUỐN:

### ✅ Cho Bạn (Admin):
- **1 lần setup** MeshCentral server
- **1 lần build** package
- **Quản lý tập trung** tất cả khách hàng
- **Update 1 lần** → áp dụng cho tất cả
- **Monitor real-time** tất cả agents

### ✅ Cho Khách Hàng:
- **Cài đặt 1 lần** → Setup tự động
- **Tự động hoạt động** → Không cần can thiệp
- **Tự động update** → XML mới từ server
- **Bảo vệ tự động** → File XML
- **Báo cáo tự động** → Lên server

## 🚀 BẮT ĐẦU NGAY:

1. **Chạy script build** trên Windows
2. **Upload ZIP** lên MeshCentral
3. **Gửi link** cho khách hàng
4. **Monitor** qua MeshCentral dashboard

---
**Admin Quick Start v2.0.0 - Triển khai dễ dàng!** 🚀✨

**Support**: admin@xmlguard.com
**MeshCentral**: https://103.69.86.130:4433