@echo off
title XML Guard Enterprise - Service Removal
color 0C

echo ========================================
echo   XML GUARD ENTERPRISE SERVICE
echo   Service Removal
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

echo [INFO] Stopping XML Guard Service...
XMLGuardService.exe stop

echo [INFO] Uninstalling XML Guard Service...
XMLGuardService.exe uninstall

echo.
echo [INFO] XML Guard Service has been removed.
echo.
pause
