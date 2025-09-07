#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Universal Agent - Tạo 1 file EXE duy nhất
Version: 2.0.0
Author: AI Assistant (Cipher)
"""

import os
import sys
import shutil
import subprocess

def main():
    print("🏗️ BUILD XML GUARD UNIVERSAL AGENT")
    print("=" * 50)
    
    # Build Universal Agent
    print("🔨 Building Universal Agent...")
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole',
        '--name=XMLGuardUniversalAgent', 
        '--clean',
        '--add-data=config.json;.',
        'xmlguard_universal_agent.py'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Build failed: {result.stderr}")
            return False
        print("✅ Universal Agent built successfully!")
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False
    
    # Tạo package directory
    package_dir = "XMLGuard_Universal_Package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy Universal Agent
    if os.path.exists("dist/XMLGuardUniversalAgent.exe"):
        shutil.copy2("dist/XMLGuardUniversalAgent.exe", f"{package_dir}/XMLGuardUniversalAgent.exe")
        print("✅ Universal Agent copied to package")
    else:
        print("❌ Universal Agent EXE not found!")
        return False
    
    # Copy config
    if os.path.exists("config.json"):
        shutil.copy2("config.json", f"{package_dir}/config.json")
        print("✅ Config copied to package")
    
    # Tạo installer
    installer_content = '''@echo off
title XML Guard Universal Agent Installation
color 0A

echo ========================================
echo   XML GUARD UNIVERSAL AGENT INSTALLATION
echo ========================================
echo.

REM Check admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Cần quyền Administrator!
    echo Right-click và chọn "Run as administrator"
    pause
    exit /b 1
)

echo [INFO] Installing XML Guard Universal Agent...
echo [INFO] Agent sẽ tự động phát hiện công ty và MST
echo [INFO] Kết nối MeshTrash server: https://103.69.86.130:4433
echo.

XMLGuardUniversalAgent.exe start

echo.
echo ========================================
echo   CÀI ĐẶT HOÀN TẤT!
echo ========================================
echo.
echo XML Guard Universal Agent đã khởi động
echo - Tự động phát hiện công ty và MST
echo - Kết nối MeshTrash server
echo - Bảo vệ file XML tự động
echo - Remote control từ MeshTrash
echo.
echo Để dừng: XMLGuardUniversalAgent.exe stop
echo Để kiểm tra: XMLGuardUniversalAgent.exe status
echo.
pause
'''
    
    with open(f"{package_dir}/Install.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    # Tạo README
    readme_content = '''XML GUARD UNIVERSAL AGENT
========================

NỘI DUNG PACKAGE:
- XMLGuardUniversalAgent.exe (Universal Agent - Tất cả trong 1 file)
- config.json (Cấu hình)
- Install.bat (Cài đặt tự động)

HƯỚNG DẪN CÀI ĐẶT:
1. Right-click "Install.bat"
2. Chọn "Run as administrator"
3. Chờ cài đặt hoàn tất

TÍNH NĂNG:
✅ Tự động phát hiện công ty và MST
✅ Kết nối MeshTrash server thật
✅ Bảo vệ file XML tự động
✅ Remote control từ MeshTrash
✅ Tất cả trong 1 file EXE duy nhất
✅ Hoàn chỉnh và cố định

SỬ DỤNG:
- XMLGuardUniversalAgent.exe start    # Khởi động
- XMLGuardUniversalAgent.exe stop     # Dừng
- XMLGuardUniversalAgent.exe status   # Kiểm tra trạng thái

MESHTRASH SERVER:
- URL: https://103.69.86.130:4433
- Tự động kết nối và đăng ký
- Remote control từ web interface

LIÊN HỆ HỖ TRỢ:
📧 Email: support@xmlguard.vn
📱 Hotline: 1900-XMLGUARD

© 2025 XML Guard Enterprise
'''
    
    with open(f"{package_dir}/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"\n🎉 UNIVERSAL PACKAGE HOÀN THÀNH!")
    print(f"📁 Thư mục: {package_dir}")
    print(f"📊 Kích thước: {get_size(package_dir):.1f} MB")
    
    print(f"\n📋 TÍNH NĂNG UNIVERSAL AGENT:")
    print(f"✅ Tự động phát hiện công ty và MST")
    print(f"✅ Kết nối MeshTrash server thật")
    print(f"✅ Bảo vệ file XML tự động")
    print(f"✅ Remote control từ MeshTrash")
    print(f"✅ Tất cả trong 1 file EXE duy nhất")
    print(f"✅ Hoàn chỉnh và cố định")
    
    print(f"\n🚀 BƯỚC TIẾP THEO:")
    print(f"1. Test Universal Agent: {package_dir}/XMLGuardUniversalAgent.exe start")
    print(f"2. Zip thư mục {package_dir}")
    print(f"3. Gửi cho khách hàng")
    print(f"4. Khách hàng chỉ cần chạy Install.bat")
    
    return True

def get_size(directory):
    """Tính kích thước thư mục (MB)"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total += os.path.getsize(filepath)
    return total / (1024 * 1024)

if __name__ == "__main__":
    main()
