@echo off
title Integrated MeshAgent + XML Guard
color 0A

echo ================================================
echo   INTEGRATED MESHAGENT + XML GUARD
echo ================================================
echo.
echo 🚀 1 FILE DUY NHẤT - MeshAgent + XML Guard!
echo.

REM Check admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Cần quyền Administrator!
    echo Right-click và chọn "Run as administrator"
    pause
    exit /b 1
)

echo [INFO] Installing Integrated MeshAgent + XML Guard...
IntegratedMeshAgent.exe install

echo [INFO] Starting protection...
IntegratedMeshAgent.exe start

echo.
echo ================================================
echo   CÀI ĐẶT HOÀN TẤT!
echo ================================================
echo.
echo ✅ MeshAgent + XML Guard đã được cài đặt
echo ✅ Kết nối MeshCentral server
echo ✅ Bảo vệ file thuế 24/7
echo ✅ Remote control và monitoring
echo.
echo 📁 Log file: C:\Windows\Temp\xmlguard_meshagent.log
echo 🌐 Server: https://103.69.86.130:4433
echo.
pause
