XML GUARD ENTERPRISE - WINDOWS SERVICE EDITION
=============================================

Build Date: 2025-09-07 13:19:21
Version: 2.0.0 SERVICE

SERVICE FEATURES:
----------------
✅ True Windows Service (not just EXE)
✅ Cannot be killed from Task Manager
✅ Auto-starts with Windows
✅ Runs with SYSTEM privileges
✅ Self-healing (restarts if crashed)
✅ Survives user logoff/reboot
✅ Professional enterprise deployment

INSTALLATION:
------------
1. Right-click "install_service.bat"
2. Select "Run as administrator"
3. Service installs and starts automatically
4. Check Windows Services (services.msc)

SERVICE MANAGEMENT:
------------------
XMLGuardService.exe install    # Install service
XMLGuardService.exe uninstall  # Remove service
XMLGuardService.exe start      # Start service
XMLGuardService.exe stop       # Stop service
XMLGuardService.exe status     # Check status

ENTERPRISE FEATURES:
-------------------
- Real-time XML protection
- Automatic file overwrite (not just quarantine)
- 4-field identification protection
- MeshCentral integration
- Company auto-detection
- Stealth operation mode

UNINSTALLATION:
--------------
1. Right-click "uninstall_service.bat"
2. Select "Run as administrator"
3. Service will be completely removed

SECURITY NOTES:
--------------
- Service runs as SYSTEM user
- Has full system access (required for protection)
- Cannot be terminated by normal users
- Survives malware/hacker attempts to kill
- Logs to Windows Event Log

TROUBLESHOOTING:
---------------
- Check Windows Event Viewer for service logs
- Use "services.msc" to verify service status
- Service name: "XML Guard Enterprise Protection Service"

© 2025 XML Guard Enterprise - SERVICE Edition
