@echo off
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
echo 📁 Log file: C:\Windows\Temp\xmlguard_universal.log
echo 🌐 Server: https://103.69.86.130:4433
echo.
pause
