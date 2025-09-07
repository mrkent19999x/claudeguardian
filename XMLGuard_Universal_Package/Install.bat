@echo off
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
