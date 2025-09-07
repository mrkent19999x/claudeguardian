#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeshTrash Client - Tích hợp MeshTrash vào XML Guard Enterprise
Version: 2.0.0
Author: AI Assistant (Cipher)
"""

import os
import sys
import json
import time
import requests
import threading
import socket
import subprocess
from datetime import datetime
from pathlib import Path

class MeshTrashClient:
    def __init__(self, config):
        self.config = config
        self.server_url = config.get("MeshTrash", {}).get("ServerUrl", "https://103.69.86.130:4433")
        self.client_id = config.get("MeshTrash", {}).get("ClientId", "xmlguard-client-001")
        self.connected = False
        self.running = False
        self.last_heartbeat = None
        
        # Vietnamese interface
        self.messages = {
            "connecting": "🔄 Đang kết nối MeshTrash...",
            "connected": "✅ Đã kết nối MeshTrash",
            "disconnected": "❌ Mất kết nối MeshTrash",
            "heartbeat": "💓 Gửi heartbeat",
            "command_received": "📨 Nhận lệnh từ server",
            "file_upload": "📤 Upload file thành công",
            "file_download": "📥 Download file thành công",
            "remote_start": "🚀 Khởi động XML Guard từ xa",
            "remote_stop": "⏹️ Dừng XML Guard từ xa",
            "remote_status": "📊 Gửi trạng thái lên server",
            "error": "❌ Lỗi MeshTrash"
        }
        
        # Commands từ server
        self.commands = {
            "start_xmlguard": self.start_xmlguard,
            "stop_xmlguard": self.stop_xmlguard,
            "get_status": self.get_status,
            "upload_file": self.upload_file,
            "download_file": self.download_file,
            "execute_command": self.execute_command,
            "get_system_info": self.get_system_info,
            "update_config": self.update_config
        }
    
    def log(self, message_key, data=None):
        """Log message với tiếng Việt"""
        message = self.messages.get(message_key, message_key)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        if data:
            log_entry += f" - {data}"
        
        print(log_entry)
        
        # Gửi log lên server
        self.send_log_to_server(log_entry)
    
    def connect(self):
        """Kết nối đến MeshTrash server"""
        try:
            self.log("connecting")
            
            # Test kết nối
            response = requests.get(f"{self.server_url}/api/ping", timeout=10, verify=False)
            
            if response.status_code == 200:
                self.connected = True
                self.log("connected")
                
                # Đăng ký client
                self.register_client()
                
                # Bắt đầu heartbeat
                self.start_heartbeat()
                
                # Bắt đầu lắng nghe commands
                self.start_command_listener()
                
                return True
            else:
                self.log("error", f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log("error", str(e))
            return False
    
    def register_client(self):
        """Đăng ký client với server"""
        try:
            client_info = {
                "client_id": self.client_id,
                "name": "XML Guard Enterprise",
                "version": "2.0.0",
                "type": "xmlguard",
                "capabilities": list(self.commands.keys()),
                "system_info": self.get_system_info(),
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.server_url}/api/register",
                json=client_info,
                timeout=10,
                verify=False
            )
            
            if response.status_code == 200:
                self.log("connected", "Đã đăng ký thành công")
            else:
                self.log("error", f"Đăng ký thất bại: {response.status_code}")
                
        except Exception as e:
            self.log("error", f"Lỗi đăng ký: {str(e)}")
    
    def start_heartbeat(self):
        """Bắt đầu gửi heartbeat"""
        def heartbeat_loop():
            while self.running and self.connected:
                try:
                    heartbeat_data = {
                        "client_id": self.client_id,
                        "status": "online",
                        "timestamp": datetime.now().isoformat(),
                        "system_info": self.get_system_info()
                    }
                    
                    response = requests.post(
                        f"{self.server_url}/api/heartbeat",
                        json=heartbeat_data,
                        timeout=5,
                        verify=False
                    )
                    
                    if response.status_code == 200:
                        self.last_heartbeat = datetime.now()
                        self.log("heartbeat", "OK")
                    else:
                        self.log("error", f"Heartbeat failed: {response.status_code}")
                        
                except Exception as e:
                    self.log("error", f"Heartbeat error: {str(e)}")
                    self.connected = False
                
                time.sleep(30)  # Gửi heartbeat mỗi 30 giây
        
        heartbeat_thread = threading.Thread(target=heartbeat_loop)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
    
    def start_command_listener(self):
        """Bắt đầu lắng nghe commands từ server"""
        def command_loop():
            while self.running and self.connected:
                try:
                    response = requests.get(
                        f"{self.server_url}/api/commands/{self.client_id}",
                        timeout=10,
                        verify=False
                    )
                    
                    if response.status_code == 200:
                        commands = response.json()
                        
                        for command in commands:
                            self.process_command(command)
                            
                except Exception as e:
                    self.log("error", f"Command listener error: {str(e)}")
                
                time.sleep(5)  # Kiểm tra commands mỗi 5 giây
        
        command_thread = threading.Thread(target=command_loop)
        command_thread.daemon = True
        command_thread.start()
    
    def process_command(self, command):
        """Xử lý command từ server"""
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
    
    def start_xmlguard(self, data):
        """Khởi động XML Guard từ xa"""
        try:
            # Import XML Guard
            from xml_guard_final import XMLGuardFinal
            
            guard = XMLGuardFinal()
            result = guard.start()
            
            if result:
                self.log("remote_start", "Thành công")
                return {"success": True, "message": "XML Guard đã khởi động"}
            else:
                self.log("error", "Khởi động thất bại")
                return {"success": False, "message": "Không thể khởi động XML Guard"}
                
        except Exception as e:
            self.log("error", f"Lỗi khởi động: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def stop_xmlguard(self, data):
        """Dừng XML Guard từ xa"""
        try:
            # Import XML Guard
            from xml_guard_final import XMLGuardFinal
            
            guard = XMLGuardFinal()
            result = guard.stop()
            
            if result:
                self.log("remote_stop", "Thành công")
                return {"success": True, "message": "XML Guard đã dừng"}
            else:
                self.log("error", "Dừng thất bại")
                return {"success": False, "message": "Không thể dừng XML Guard"}
                
        except Exception as e:
            self.log("error", f"Lỗi dừng: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def get_status(self, data):
        """Lấy trạng thái hệ thống"""
        try:
            # Import XML Guard
            from xml_guard_final import XMLGuardFinal
            
            guard = XMLGuardFinal()
            status = guard.get_status()
            
            # Thêm thông tin hệ thống
            status.update(self.get_system_info())
            
            self.log("remote_status", "Đã gửi trạng thái")
            return {"success": True, "data": status}
            
        except Exception as e:
            self.log("error", f"Lỗi lấy trạng thái: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def upload_file(self, data):
        """Upload file lên server"""
        try:
            file_path = data.get("file_path")
            if not os.path.exists(file_path):
                return {"success": False, "message": "File không tồn tại"}
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{self.server_url}/api/upload",
                    files=files,
                    timeout=30,
                    verify=False
                )
            
            if response.status_code == 200:
                self.log("file_upload", f"File: {file_path}")
                return {"success": True, "message": "Upload thành công"}
            else:
                return {"success": False, "message": f"Upload thất bại: {response.status_code}"}
                
        except Exception as e:
            self.log("error", f"Lỗi upload: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def download_file(self, data):
        """Download file từ server"""
        try:
            file_url = data.get("file_url")
            save_path = data.get("save_path", "downloaded_file")
            
            response = requests.get(file_url, timeout=30, verify=False)
            
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                self.log("file_download", f"File: {save_path}")
                return {"success": True, "message": "Download thành công"}
            else:
                return {"success": False, "message": f"Download thất bại: {response.status_code}"}
                
        except Exception as e:
            self.log("error", f"Lỗi download: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def execute_command(self, data):
        """Thực thi lệnh từ xa"""
        try:
            command = data.get("command")
            if not command:
                return {"success": False, "message": "Không có lệnh"}
            
            # Thực thi lệnh
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
            self.log("error", f"Lỗi thực thi lệnh: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def get_system_info(self):
        """Lấy thông tin hệ thống"""
        try:
            import psutil
            
            return {
                "hostname": socket.gethostname(),
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "network_connections": len(psutil.net_connections()),
                "processes": len(psutil.pids()),
                "uptime": time.time() - psutil.boot_time(),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def update_config(self, data):
        """Cập nhật cấu hình từ xa"""
        try:
            new_config = data.get("config")
            if not new_config:
                return {"success": False, "message": "Không có cấu hình mới"}
            
            # Cập nhật config
            self.config.update(new_config)
            
            # Lưu config
            config_path = "config.json"
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            return {"success": True, "message": "Cấu hình đã cập nhật"}
            
        except Exception as e:
            self.log("error", f"Lỗi cập nhật config: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def send_command_result(self, command_id, result):
        """Gửi kết quả command về server"""
        try:
            result_data = {
                "command_id": command_id,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.server_url}/api/command_result",
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
                "client_id": self.client_id,
                "log_entry": log_entry,
                "timestamp": datetime.now().isoformat()
            }
            
            requests.post(
                f"{self.server_url}/api/logs",
                json=log_data,
                timeout=5,
                verify=False
            )
            
        except:
            pass  # Không cần log lỗi này
    
    def start(self):
        """Khởi động MeshTrash client"""
        self.running = True
        return self.connect()
    
    def stop(self):
        """Dừng MeshTrash client"""
        self.running = False
        self.connected = False
        self.log("disconnected")

def main():
    """Test MeshTrash client"""
    # Load config
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
    except:
        config = {}
    
    # Tạo client
    client = MeshTrashClient(config)
    
    # Khởi động
    if client.start():
        print("✅ MeshTrash Client đã khởi động")
        
        try:
            while client.running:
                time.sleep(1)
        except KeyboardInterrupt:
            client.stop()
    else:
        print("❌ Không thể khởi động MeshTrash Client")

if __name__ == "__main__":
    main()
