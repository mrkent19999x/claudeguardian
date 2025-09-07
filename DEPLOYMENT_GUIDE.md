# 🚀 XML Guard Universal - Deployment Guide

## 📋 **TỔNG QUAN**

XML Guard Universal là giải pháp **1 FILE DUY NHẤT** để bảo vệ file XML thuế, tích hợp hoàn toàn với MeshTrash server làm trung tâm điều khiển.

---

## 🎯 **CHO KHÁCH HÀNG - SIÊU ĐƠN GIẢN**

### **✅ Chỉ cần 1 file:**
```
XMLGuardUniversal.exe (20MB)
```

### **✅ Cài đặt 1 click:**
1. Right-click `XMLGuardUniversal.exe`
2. Chọn "Run as administrator"
3. Xong! Hệ thống được bảo vệ

### **✅ Tự động:**
- Cài đặt Windows Service
- Kết nối MeshTrash server
- Bảo vệ file XML thuế 24/7
- Tự động update từ server
- Không cần config gì

---

## 🎯 **CHO ANH NGHĨA - QUẢN LÝ TẬP TRUNG**

### **✅ MeshTrash Server:**
```bash
# Chạy server
python meshtrash_server_enhanced.py

# Truy cập dashboard
http://localhost:5000
```

### **✅ Quản lý từ dashboard:**
- **Upload file gốc** - Drag & drop XML files
- **Monitor clients** - Xem status tất cả máy
- **Deploy updates** - Cập nhật tự động
- **View logs** - Logs real-time từ tất cả client

### **✅ API Endpoints:**
- `/api/heartbeat` - Nhận heartbeat từ clients
- `/api/legitimate_files` - Cung cấp file gốc
- `/api/upload_files` - Upload file gốc
- `/api/check_update` - Kiểm tra updates
- `/api/deploy_update` - Deploy updates

---

## 🔧 **KIẾN TRÚC HỆ THỐNG**

### **Client Side (XMLGuardUniversal.exe):**
```
┌─────────────────────────────────────┐
│  XMLGuardUniversal.exe (20MB)       │
├─────────────────────────────────────┤
│  ✅ Embedded Config                 │
│  ✅ MeshTrash Client                │
│  ✅ XML Protection Engine          │
│  ✅ Windows Service                 │
│  ✅ Auto-Update System             │
│  ✅ Self-Protection                │
└─────────────────────────────────────┘
```

### **Server Side (MeshTrash Server):**
```
┌─────────────────────────────────────┐
│  MeshTrash Universal Server         │
├─────────────────────────────────────┤
│  ✅ Web Dashboard                   │
│  ✅ SQLite Database                 │
│  ✅ File Management                 │
│  ✅ Client Monitoring               │
│  ✅ Update Deployment               │
│  ✅ Log Aggregation                 │
└─────────────────────────────────────┘
```

---

## 📦 **DEPLOYMENT OPTIONS**

### **Option 1: EXE File (Recommended)**
```bash
# Gửi cho khách hàng:
XMLGuardUniversal.exe (20MB)

# Khách hàng chỉ cần:
Right-click → Run as administrator
```

### **Option 2: MSI Package**
```bash
# Tạo MSI installer:
candle XMLGuardUniversal.wxs
light XMLGuardUniversal.wixobj

# Gửi cho khách hàng:
XMLGuardUniversal.msi (25MB)

# Khách hàng chỉ cần:
Double-click MSI file
```

### **Option 3: Silent Installation**
```bash
# Deploy tự động:
msiexec /i XMLGuardUniversal.msi /quiet

# Hoặc qua Group Policy
```

---

## 🌐 **MESHTRASH INTEGRATION**

### **Client → Server Communication:**
```python
# Heartbeat (mỗi 60 giây)
POST /api/heartbeat
{
    "client_id": "COMPUTER-NAME",
    "status": "running",
    "version": "3.0.0"
}

# Request file gốc
POST /api/legitimate_files
{
    "mst": "0401985971",
    "form_code": "842",
    "period": "2/2025",
    "action": "get_legitimate_path"
}

# Check updates (mỗi giờ)
POST /api/check_update
{
    "current_version": "3.0.0"
}
```

### **Server → Client Response:**
```python
# File gốc response
{
    "success": true,
    "file_path": "/path/to/legitimate/file.xml"
}

# Update response
{
    "update_available": true,
    "new_version": "3.1.0",
    "download_url": "https://server.com/update.exe"
}
```

---

## 🚀 **QUY TRÌNH DEPLOYMENT**

### **Bước 1: Setup Server**
```bash
# 1. Chạy MeshTrash server
python meshtrash_server_enhanced.py

# 2. Upload file gốc qua dashboard
# 3. Configure client settings
```

### **Bước 2: Build Client**
```bash
# 1. Build Universal EXE
python build_universal.py

# 2. Test EXE locally
XMLGuardUniversal.exe start

# 3. Package for deployment
```

### **Bước 3: Deploy to Clients**
```bash
# 1. Gửi XMLGuardUniversal.exe cho khách
# 2. Hướng dẫn chạy với quyền admin
# 3. Monitor qua dashboard
```

### **Bước 4: Monitor & Maintain**
```bash
# 1. Xem status clients trên dashboard
# 2. Upload file gốc mới khi cần
# 3. Deploy updates khi có
# 4. Xem logs để troubleshoot
```

---

## 📊 **MONITORING & MAINTENANCE**

### **Dashboard Features:**
- **Real-time client status**
- **File upload interface**
- **Update deployment**
- **Log viewing**
- **Statistics**

### **Automated Tasks:**
- **Heartbeat monitoring**
- **Auto-update deployment**
- **Log aggregation**
- **File synchronization**

---

## 🎉 **LỢI ÍCH**

### **✅ Cho Khách Hàng:**
- **1 file duy nhất** - không phức tạp
- **Cài 1 lần chạy mãi** - zero maintenance
- **Tự động update** - luôn có version mới
- **Bảo vệ 24/7** - không cần can thiệp

### **✅ Cho Anh Nghĩa:**
- **Centralized control** - quản lý từ 1 nơi
- **Easy deployment** - gửi 1 file
- **Real-time monitoring** - biết status mọi client
- **Automated updates** - không cần support thủ công
- **Scalable** - dễ mở rộng thêm client

---

## 📞 **SUPPORT**

- **Email:** support@xmlguard.vn
- **Hotline:** 1900-XMLGUARD
- **GitHub:** https://github.com/mrkent19999x/claudeguardian

---

**© 2025 XML Guard Universal - Built by Cipher AI** 🚀
