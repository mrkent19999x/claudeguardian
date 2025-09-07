@echo off
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
