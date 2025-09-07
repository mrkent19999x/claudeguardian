#!/usr/bin/env python3
"""
Build package đơn giản - không cần MeshAgent trước
"""

import os
import sys
import shutil
import subprocess

def main():
    print("🏗️ BUILD XML GUARD PACKAGE")
    print("=" * 40)
    
    # Build XML Guard
    print("🔨 Building XML Guard...")
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole',
        '--name=XMLGuardEnterprise', 
        '--clean',
        'xml_guard_final.py'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Build failed: {result.stderr}")
            return False
        print("✅ XML Guard built successfully!")
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False
    
    # Tạo package directory
    package_dir = "XMLGuard_Enterprise_Package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy XML Guard
    if os.path.exists("dist/XMLGuardEnterprise.exe"):
        shutil.copy2("dist/XMLGuardEnterprise.exe", f"{package_dir}/XMLGuardEnterprise.exe")
        print("✅ XML Guard copied to package")
    else:
        print("❌ XML Guard EXE not found!")
        return False
    
    # Tạo installer
    installer_content = '''@echo off
title XML Guard Enterprise Installation
color 0A

echo ========================================
echo   XML GUARD ENTERPRISE INSTALLATION
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

echo [INFO] Installing XML Guard Enterprise...
XMLGuardEnterprise.exe install

echo [INFO] Starting protection...
XMLGuardEnterprise.exe start

echo.
echo ========================================
echo   CÀI ĐẶT HOÀN TẤT!
echo ========================================
echo.
echo Hệ thống đã được bảo vệ bởi XML Guard Enterprise
echo File thuế của bạn được bảo vệ 24/7
echo.
pause
'''
    
    with open(f"{package_dir}/Install.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    # Tạo README
    readme_content = '''XML GUARD ENTERPRISE
==================

NỘI DUNG PACKAGE:
- XMLGuardEnterprise.exe (Bảo vệ file XML thuế)
- Install.bat (Cài đặt tự động)

HƯỚNG DẪN CÀI ĐẶT:
1. Right-click "Install.bat"
2. Chọn "Run as administrator"
3. Chờ cài đặt hoàn tất

TÍNH NĂNG:
- Bảo vệ file XML thuế real-time
- Tự động ghi đè file fake bằng file gốc
- Chạy như Windows Service
- Không thể bị tắt bởi malware

LIÊN HỆ HỖ TRỢ:
📧 Email: support@xmlguard.vn
📱 Hotline: 1900-XMLGUARD

© 2025 XML Guard Enterprise
'''
    
    with open(f"{package_dir}/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"\n🎉 PACKAGE HOÀN THÀNH!")
    print(f"📁 Thư mục: {package_dir}")
    print(f"📊 Kích thước: {get_size(package_dir):.1f} MB")
    
    print(f"\n📋 BƯỚC TIẾP THEO:")
    print(f"1. Copy MeshAgent.exe vào thư mục {package_dir}")
    print(f"2. Zip thư mục {package_dir}")
    print(f"3. Gửi cho khách hàng")
    
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

