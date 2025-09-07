@echo off
title XML Guard Enterprise - Installer
color 0A

echo ========================================
echo   XML GUARD ENTERPRISE v2.0.0
echo   Universal Installer
echo ========================================
echo.

REM Check admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] This installer requires administrator privileges!
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Create installation directory
set INSTALL_DIR=C:\XMLGuard
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy EXE
echo [INFO] Installing XML Guard Enterprise...
copy "XMLGuardEnterprise.exe" "%INSTALL_DIR%\XMLGuardEnterprise.exe"

REM Create desktop shortcut (optional)
echo [INFO] Creating shortcuts...
echo Set WshShell = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo Set Shortcut = WshShell.CreateShortcut("%USERPROFILE%\Desktop\XML Guard Enterprise.lnk") >> CreateShortcut.vbs
echo Shortcut.TargetPath = "%INSTALL_DIR%\XMLGuardEnterprise.exe" >> CreateShortcut.vbs
echo Shortcut.WorkingDirectory = "%INSTALL_DIR%" >> CreateShortcut.vbs
echo Shortcut.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs >nul
del CreateShortcut.vbs

REM Start service
echo [INFO] Starting XML Guard Enterprise...
cd /d "%INSTALL_DIR%"
start "" "XMLGuardEnterprise.exe"

echo.
echo ========================================
echo   INSTALLATION COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo XML Guard Enterprise is now running...
echo Check desktop shortcut for future use.
echo.
pause
