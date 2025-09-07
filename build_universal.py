#!/usr/bin/env python3
"""
Build XML Guard Universal - 1 FILE DUY NHẤT
Tạo EXE hoàn toàn độc lập, không cần file ngoài
"""

import os
import sys
import shutil
import subprocess

def main():
    print("🏗️ BUILDING XML GUARD UNIVERSAL")
    print("=" * 50)
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Build command for PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',                    # 1 file duy nhất
        '--noconsole',                  # Không hiện console
        '--name=XMLGuardUniversal',     # Tên file EXE
        '--clean',                      # Clean build
        '--add-data=README.md;.',       # Embed README
        'xml_guard_universal.py'        # File Python chính
    ]
    
    print("🔨 Building Universal EXE...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Build failed: {result.stderr}")
            return False
        print("✅ Universal EXE built successfully!")
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False
    
    # Check if EXE was created
    exe_path = "dist/XMLGuardUniversal.exe"
    if not os.path.exists(exe_path):
        print("❌ EXE file not found!")
        return False
    
    # Get file size
    file_size = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"📊 EXE size: {file_size:.1f} MB")
    
    # Create deployment package
    package_dir = "XMLGuard_Universal_Package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy EXE to package
    shutil.copy2(exe_path, f"{package_dir}/XMLGuardUniversal.exe")
    
    # Create installer script
    installer_content = '''@echo off
title XML Guard Universal - 1 File Solution
color 0A

echo ================================================
echo   XML GUARD UNIVERSAL - 1 FILE SOLUTION
echo ================================================
echo.
echo 🚀 Cài đặt tự động - Chỉ cần 1 file duy nhất!
echo.

REM Check admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Cần quyền Administrator!
    echo Right-click và chọn "Run as administrator"
    pause
    exit /b 1
)

echo [INFO] Installing XML Guard Universal Service...
XMLGuardUniversal.exe install

echo [INFO] Starting protection...
XMLGuardUniversal.exe start

echo.
echo ================================================
echo   CÀI ĐẶT HOÀN TẤT!
echo ================================================
echo.
echo ✅ XML Guard Universal đã được cài đặt
echo ✅ Bảo vệ file thuế 24/7
echo ✅ Tự động kết nối MeshTrash
echo ✅ Không cần config thủ công
echo.
echo 📁 Log file: C:\\Windows\\Temp\\xmlguard_universal.log
echo 🌐 Server: https://103.69.86.130:4433
echo.
pause
'''
    
    with open(f"{package_dir}/Install.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    # Create README
    readme_content = '''XML GUARD UNIVERSAL v3.0.0
=============================

🎯 1 FILE DUY NHẤT - KHÔNG CẦN GÌ KHÁC!

NỘI DUNG:
- XMLGuardUniversal.exe (Bảo vệ file XML thuế)
- Install.bat (Cài đặt tự động)

🚀 CÁCH SỬ DỤNG:
1. Right-click "Install.bat"
2. Chọn "Run as administrator"
3. Xong! Hệ thống được bảo vệ

✨ TÍNH NĂNG:
- 1 file EXE duy nhất (không cần Python)
- Tự động cài đặt Windows Service
- Tự động kết nối MeshTrash server
- Bảo vệ file XML thuế real-time
- Tự động ghi đè file fake
- Chạy ẩn như system process
- Không thể bị tắt bởi malware
- Tự động update từ server

🌐 MESHTRASH INTEGRATION:
- Server: https://103.69.86.130:4433
- Tự động lấy file gốc từ database
- Remote monitoring và control
- Auto-update system

📞 HỖ TRỢ:
📧 Email: support@xmlguard.vn
📱 Hotline: 1900-XMLGUARD

© 2025 XML Guard Universal - Built by Cipher AI
'''
    
    with open(f"{package_dir}/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Create MSI installer script
    msi_script = '''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="XML Guard Universal" Language="1033" Version="3.0.0" Manufacturer="Cipher AI" UpgradeCode="PUT-GUID-HERE">
    <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />
    
    <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />
    <MediaTemplate />
    
    <Feature Id="ProductFeature" Title="XML Guard Universal" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
    </Feature>
    
    <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
      <Component Id="MainExecutable" Guid="*">
        <File Id="XMLGuardUniversal.exe" Source="XMLGuardUniversal.exe" KeyPath="yes" />
      </Component>
    </ComponentGroup>
  </Product>
  
  <Fragment>
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="XMLGuardUniversal" />
      </Directory>
    </Directory>
  </Fragment>
</Wix>'''
    
    with open(f"{package_dir}/XMLGuardUniversal.wxs", "w", encoding="utf-8") as f:
        f.write(msi_script)
    
    print(f"\n🎉 UNIVERSAL PACKAGE HOÀN THÀNH!")
    print(f"📁 Thư mục: {package_dir}")
    print(f"📊 Kích thước: {get_size(package_dir):.1f} MB")
    
    print(f"\n📋 BƯỚC TIẾP THEO:")
    print(f"1. Test EXE: {package_dir}/XMLGuardUniversal.exe")
    print(f"2. Test Installer: {package_dir}/Install.bat")
    print(f"3. Tạo MSI: candle + light {package_dir}/XMLGuardUniversal.wxs")
    print(f"4. Deploy cho khách hàng!")
    
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
