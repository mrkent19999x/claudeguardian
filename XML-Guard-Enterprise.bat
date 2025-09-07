@echo off
title XML Guard Enterprise v2.0.0
color 0A

echo.
echo ========================================
echo   XML GUARD ENTERPRISE v2.0.0
echo   Complete Protection System
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] This program requires administrator privileges!
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Set working directory
cd /d "%~dp0"

REM Check Python installation
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Install Python dependencies
echo [INFO] Installing required packages...
python -m pip install requests psutil --quiet --disable-pip-version-check --user
if %errorLevel% neq 0 (
    echo [WARN] Some packages may not install correctly, but continuing...
)

REM Start XML Guard
echo [INFO] Starting XML Guard Enterprise...
python "xml_guard_final.py" start

REM Keep window open
echo.
echo [INFO] XML Guard is running in the background...
echo [INFO] Press any key to stop...
pause >nul

REM Stop XML Guard
echo [INFO] Stopping XML Guard...
python "xml_guard_final.py" stop

echo [INFO] XML Guard stopped. Goodbye!
pause
