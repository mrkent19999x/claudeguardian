@echo off
title XML Guard Enterprise - Service Installation
color 0A

echo ========================================
echo   XML GUARD ENTERPRISE SERVICE
echo   Windows Service Installation
echo ========================================
echo.

REM Check admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Administrative privileges required!
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo [INFO] Installing XML Guard Enterprise Service...

REM Install Windows Service
XMLGuardService.exe install
if %errorLevel% neq 0 (
    echo [ERROR] Service installation failed!
    pause
    exit /b 1
)

echo [INFO] Starting XML Guard Service...
XMLGuardService.exe start
if %errorLevel% neq 0 (
    echo [WARN] Service start failed - try manually
)

echo.
echo ========================================
echo   SERVICE INSTALLATION COMPLETED!
echo ========================================
echo.
echo XML Guard is now running as Windows Service
echo - Cannot be killed from Task Manager
echo - Auto-starts with Windows
echo - Runs with SYSTEM privileges
echo.
echo To manage service:
echo   XMLGuardService.exe status
echo   XMLGuardService.exe stop
echo   XMLGuardService.exe start
echo   XMLGuardService.exe uninstall
echo.
pause
