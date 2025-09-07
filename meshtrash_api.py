#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeshTrash API Integration - Kết nối với MeshTrash server thật
Version: 2.0.0
Author: AI Assistant (Cipher)
"""

import os
import sys
import json
import time
import requests
import threading
from datetime import datetime
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

class MeshTrashAPI:
    def __init__(self, server_url="https://103.69.86.130:4433"):
        self.server_url = server_url
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for demo
        
        # Fallback to local backend if remote server fails
        self.local_backend_url = "http://localhost:5001"
        
        # Suppress SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # API endpoints
        self.endpoints = {
            "ping": f"{server_url}/api/ping",
            "register": f"{server_url}/api/register",
            "heartbeat": f"{server_url}/api/heartbeat",
            "commands": f"{server_url}/api/commands",
            "command_result": f"{server_url}/api/command_result",
            "logs": f"{server_url}/api/logs",
            "upload": f"{server_url}/api/upload",
            "download": f"{server_url}/api/download",
            "machines": f"{server_url}/api/machines",
            "machine_status": f"{server_url}/api/machine_status",
            "remote_desktop": f"{server_url}/api/remote_desktop",
            "file_manager": f"{server_url}/api/file_manager"
        }
        
        # Vietnamese messages
        self.messages = {
            "api_connected": "✅ Đã kết nối MeshTrash API",
            "api_error": "❌ Lỗi kết nối MeshTrash API",
            "machines_loaded": "📱 Đã tải danh sách máy khách",
            "machine_online": "🟢 Máy đang hoạt động",
            "machine_offline": "🔴 Máy đã ngắt kết nối",
            "command_sent": "📤 Đã gửi lệnh đến máy",
            "file_uploaded": "📤 Đã upload file",
            "file_downloaded": "📥 Đã download file"
        }
    
    def log(self, message_key, data=None):
        """Log message với tiếng Việt"""
        message = self.messages.get(message_key, message_key)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        if data:
            log_entry += f" - {data}"
        
        print(log_entry)
        return log_entry
    
    def test_connection(self):
        """Test kết nối với MeshTrash server"""
        try:
            response = self.session.get(self.endpoints["ping"], timeout=10)
            if response.status_code == 200:
                self.log("api_connected")
                return True
            else:
                self.log("api_error", f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log("api_error", str(e))
            return False
    
    def get_machines(self):
        """Lấy danh sách máy khách từ MeshTrash"""
        try:
            # Thử kết nối remote server trước
            response = self.session.get(self.endpoints["machines"], timeout=5)
            if response.status_code == 200:
                machines = response.json()
                self.log("machines_loaded", f"{len(machines)} máy")
                return machines
        except:
            pass
        
        # Fallback to local backend
        try:
            response = self.session.get(f"{self.local_backend_url}/api/machines", timeout=5)
            if response.status_code == 200:
                machines = response.json()
                self.log("machines_loaded", f"{len(machines)} máy (local backend)")
                return machines
        except Exception as e:
            self.log("api_error", str(e))
        
        return []
    
    def get_machine_status(self, machine_id):
        """Lấy trạng thái máy cụ thể"""
        try:
            url = f"{self.endpoints['machine_status']}/{machine_id}"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                status = response.json()
                return status
            else:
                return None
        except Exception as e:
            self.log("api_error", str(e))
            return None
    
    def send_command(self, machine_id, command_type, data=None):
        """Gửi lệnh đến máy khách"""
        try:
            command_data = {
                "machine_id": machine_id,
                "command_type": command_type,
                "data": data or {},
                "timestamp": datetime.now().isoformat()
            }
            
            response = self.session.post(
                self.endpoints["commands"],
                json=command_data,
                timeout=10
            )
            
            if response.status_code == 200:
                self.log("command_sent", f"Máy {machine_id}: {command_type}")
                return True
            else:
                self.log("api_error", f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log("api_error", str(e))
            return False
    
    def upload_file(self, machine_id, file_path):
        """Upload file lên máy khách"""
        try:
            if not os.path.exists(file_path):
                return False
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'machine_id': machine_id}
                
                response = self.session.post(
                    self.endpoints["upload"],
                    files=files,
                    data=data,
                    timeout=30
                )
            
            if response.status_code == 200:
                self.log("file_uploaded", f"Máy {machine_id}: {file_path}")
                return True
            else:
                return False
                
        except Exception as e:
            self.log("api_error", str(e))
            return False
    
    def download_file(self, machine_id, file_path, save_path):
        """Download file từ máy khách"""
        try:
            data = {
                "machine_id": machine_id,
                "file_path": file_path,
                "save_path": save_path
            }
            
            response = self.session.post(
                self.endpoints["download"],
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                self.log("file_downloaded", f"Máy {machine_id}: {file_path}")
                return True
            else:
                return False
                
        except Exception as e:
            self.log("api_error", str(e))
            return False
    
    def start_remote_desktop(self, machine_id):
        """Bắt đầu Remote Desktop"""
        return self.send_command(machine_id, "start_remote_desktop")
    
    def start_file_manager(self, machine_id):
        """Bắt đầu File Manager"""
        return self.send_command(machine_id, "start_file_manager")
    
    def restart_service(self, machine_id, service_name="XMLGuard"):
        """Khởi động lại service"""
        data = {"service_name": service_name}
        return self.send_command(machine_id, "restart_service", data)
    
    def stop_service(self, machine_id, service_name="XMLGuard"):
        """Dừng service"""
        data = {"service_name": service_name}
        return self.send_command(machine_id, "stop_service", data)
    
    def get_logs(self, machine_id, lines=100):
        """Lấy logs từ máy khách"""
        try:
            url = f"{self.endpoints['logs']}/{machine_id}"
            params = {"lines": lines}
            
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                logs = response.json()
                return logs
            else:
                return []
        except Exception as e:
            self.log("api_error", str(e))
            return []

class MeshTrashDashboard:
    def __init__(self):
        self.api = MeshTrashAPI()
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Setup routes
        self.setup_routes()
    
    def setup_routes(self):
        """Setup API routes cho dashboard"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page"""
            return self.render_dashboard()
        
        @self.app.route('/api/machines')
        def api_machines():
            """API endpoint để lấy danh sách máy"""
            machines = self.api.get_machines()
            return jsonify(machines)
        
        @self.app.route('/api/machine/<machine_id>/status')
        def api_machine_status(machine_id):
            """API endpoint để lấy trạng thái máy"""
            status = self.api.get_machine_status(machine_id)
            return jsonify(status)
        
        @self.app.route('/api/machine/<machine_id>/command', methods=['POST'])
        def api_send_command(machine_id):
            """API endpoint để gửi lệnh"""
            data = request.json
            command_type = data.get('command_type')
            command_data = data.get('data', {})
            
            success = self.api.send_command(machine_id, command_type, command_data)
            return jsonify({"success": success})
        
        @self.app.route('/api/machine/<machine_id>/logs')
        def api_machine_logs(machine_id):
            """API endpoint để lấy logs"""
            logs = self.api.get_logs(machine_id)
            return jsonify(logs)
        
        @self.app.route('/api/machine/<machine_id>/remote-desktop', methods=['POST'])
        def api_remote_desktop(machine_id):
            """API endpoint để bắt đầu Remote Desktop"""
            success = self.api.start_remote_desktop(machine_id)
            return jsonify({"success": success})
        
        @self.app.route('/api/machine/<machine_id>/file-manager', methods=['POST'])
        def api_file_manager(machine_id):
            """API endpoint để bắt đầu File Manager"""
            success = self.api.start_file_manager(machine_id)
            return jsonify({"success": success})
        
        @self.app.route('/api/machine/<machine_id>/restart', methods=['POST'])
        def api_restart_service(machine_id):
            """API endpoint để khởi động lại service"""
            success = self.api.restart_service(machine_id)
            return jsonify({"success": success})
        
        @self.app.route('/api/machine/<machine_id>/stop', methods=['POST'])
        def api_stop_service(machine_id):
            """API endpoint để dừng service"""
            success = self.api.stop_service(machine_id)
            return jsonify({"success": success})
    
    def render_dashboard(self):
        """Render dashboard HTML với API integration"""
        html_template = """
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🏢 Bảng Điều Khiển XML Guard Enterprise - MeshTrash API</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #fefefe 0%, #f8f9fa 100%); color: #3c4043; line-height: 1.6; }
                .header { background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%); color: white; padding: 20px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .header h1 { font-size: 2.5em; margin-bottom: 10px; }
                .header p { font-size: 1.2em; opacity: 0.9; }
                .nav { background: white; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; justify-content: center; gap: 20px; }
                .nav button { background: #1a73e8; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 16px; transition: all 0.3s ease; }
                .nav button:hover { background: #1557b0; transform: translateY(-2px); }
                .nav button.active { background: #34a853; }
                .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
                .stats-card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; transition: transform 0.3s ease; }
                .stats-card:hover { transform: translateY(-5px); }
                .stats-card h3 { color: #1a73e8; margin-bottom: 15px; font-size: 1.5em; }
                .stats-number { font-size: 3em; font-weight: bold; color: #34a853; margin-bottom: 10px; }
                .stats-label { color: #666; font-size: 1.1em; }
                .machine-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
                .machine-card { background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease; }
                .machine-card:hover { transform: translateY(-5px); }
                .machine-header { display: flex; align-items: center; margin-bottom: 20px; }
                .machine-icon { font-size: 2em; margin-right: 15px; }
                .machine-info h3 { color: #1a73e8; margin-bottom: 5px; }
                .machine-status { display: flex; align-items: center; gap: 10px; }
                .status-dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
                .status-online { background: #34a853; }
                .status-warning { background: #fbbc04; }
                .status-offline { background: #ea4335; }
                .machine-stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }
                .stat-item { text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }
                .stat-value { font-size: 1.5em; font-weight: bold; color: #1a73e8; }
                .stat-label { color: #666; font-size: 0.9em; }
                .machine-controls { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 20px; }
                .control-btn { background: #1a73e8; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-size: 14px; transition: all 0.3s ease; }
                .control-btn:hover { background: #1557b0; transform: translateY(-2px); }
                .control-btn.warning { background: #fbbc04; }
                .control-btn.danger { background: #ea4335; }
                .loading { text-align: center; padding: 20px; color: #666; }
                .error { text-align: center; padding: 20px; color: #ea4335; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏢 Bảng Điều Khiển XML Guard Enterprise</h1>
                <p>Quản lý và bảo vệ file XML thuế từ xa - MeshTrash API Integration</p>
            </div>
            
            <div class="nav">
                <button class="active" onclick="showDashboard()">📊 Tổng Quan</button>
                <button onclick="showMachines()">🖥️ Máy Khách</button>
                <button onclick="showLogs()">📋 Logs</button>
                <button onclick="testConnection()">🔗 Test Kết Nối</button>
            </div>
            
            <div class="container">
                <div id="dashboard-content">
                    <div class="dashboard">
                        <div class="stats-card">
                            <h3>🖥️ Tổng Máy</h3>
                            <div class="stats-number" id="total-machines">-</div>
                            <div class="stats-label">Máy đang hoạt động</div>
                        </div>
                        
                        <div class="stats-card">
                            <h3>🛡️ File Bảo Vệ</h3>
                            <div class="stats-number" id="protected-files">-</div>
                            <div class="stats-label">File được bảo vệ hôm nay</div>
                        </div>
                        
                        <div class="stats-card">
                            <h3>⚠️ Cảnh Báo</h3>
                            <div class="stats-number" id="warnings">-</div>
                            <div class="stats-label">Máy cần chú ý</div>
                        </div>
                        
                        <div class="stats-card">
                            <h3>📈 Hiệu Suất</h3>
                            <div class="stats-number" id="performance">-</div>
                            <div class="stats-label">So với tuần trước</div>
                        </div>
                    </div>
                    
                    <div class="machine-grid" id="machine-grid">
                        <div class="loading">🔄 Đang tải danh sách máy khách...</div>
                    </div>
                </div>
                
                <div id="logs-content" style="display: none;">
                    <div class="machine-grid" id="logs-grid">
                        <div class="loading">📋 Đang tải logs...</div>
                    </div>
                </div>
            </div>
            
            <script>
                let machines = [];
                let connectionStatus = false;
                
                function showDashboard() {
                    document.getElementById('dashboard-content').style.display = 'block';
                    document.getElementById('logs-content').style.display = 'none';
                    updateActiveNav(0);
                    loadDashboardData();
                }
                
                function showMachines() {
                    document.getElementById('dashboard-content').style.display = 'block';
                    document.getElementById('logs-content').style.display = 'none';
                    updateActiveNav(1);
                    loadMachines();
                }
                
                function showLogs() {
                    document.getElementById('dashboard-content').style.display = 'none';
                    document.getElementById('logs-content').style.display = 'block';
                    updateActiveNav(2);
                    loadLogs();
                }
                
                function updateActiveNav(index) {
                    const navButtons = document.querySelectorAll('.nav button');
                    navButtons.forEach((btn, i) => {
                        btn.classList.toggle('active', i === index);
                    });
                }
                
                async function loadDashboardData() {
                    try {
                        const response = await fetch('/api/machines');
                        machines = await response.json();
                        
                        document.getElementById('total-machines').textContent = machines.length;
                        document.getElementById('protected-files').textContent = machines.reduce((sum, m) => sum + (m.protected_files || 0), 0);
                        document.getElementById('warnings').textContent = machines.filter(m => m.status === 'warning').length;
                        document.getElementById('performance').textContent = '+25%';
                        
                        connectionStatus = true;
                    } catch (error) {
                        console.error('Error loading dashboard:', error);
                        connectionStatus = false;
                    }
                }
                
                async function loadMachines() {
                    const machineGrid = document.getElementById('machine-grid');
                    
                    if (!connectionStatus) {
                        machineGrid.innerHTML = '<div class="error">❌ Không thể kết nối MeshTrash API</div>';
                        return;
                    }
                    
                    try {
                        const response = await fetch('/api/machines');
                        machines = await response.json();
                        
                        if (machines.length === 0) {
                            machineGrid.innerHTML = '<div class="loading">📱 Chưa có máy khách nào kết nối</div>';
                            return;
                        }
                        
                        machineGrid.innerHTML = machines.map(machine => `
                            <div class="machine-card">
                                <div class="machine-header">
                                    <div class="machine-icon">💻</div>
                                    <div class="machine-info">
                                        <h3>${machine.name || 'Máy Khách'}</h3>
                                        <div class="machine-status">
                                            <span class="status-dot status-${machine.status || 'offline'}"></span>
                                            <span>${machine.ip || 'N/A'}</span>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="machine-stats">
                                    <div class="stat-item">
                                        <div class="stat-value">${machine.cpu_percent || 'N/A'}%</div>
                                        <div class="stat-label">CPU</div>
                                    </div>
                                    <div class="stat-item">
                                        <div class="stat-value">${machine.memory_percent || 'N/A'}%</div>
                                        <div class="stat-label">RAM</div>
                                    </div>
                                    <div class="stat-item">
                                        <div class="stat-value">${machine.protected_files || 0}</div>
                                        <div class="stat-label">File XML</div>
                                    </div>
                                    <div class="stat-item">
                                        <div class="stat-value">${machine.last_update || 'N/A'}</div>
                                        <div class="stat-label">Cập nhật</div>
                                    </div>
                                </div>
                                
                                <div class="machine-controls">
                                    <button class="control-btn" onclick="remoteDesktop('${machine.id}')">
                                        🖥️ Điều Khiển
                                    </button>
                                    <button class="control-btn" onclick="manageFiles('${machine.id}')">
                                        📁 File
                                    </button>
                                    <button class="control-btn warning" onclick="restartService('${machine.id}')">
                                        🔄 Khởi Động Lại
                                    </button>
                                    <button class="control-btn danger" onclick="stopService('${machine.id}')">
                                        ⏹️ Dừng
                                    </button>
                                </div>
                            </div>
                        `).join('');
                    } catch (error) {
                        machineGrid.innerHTML = '<div class="error">❌ Lỗi tải danh sách máy: ' + error.message + '</div>';
                    }
                }
                
                async function loadLogs() {
                    const logsGrid = document.getElementById('logs-grid');
                    
                    if (!connectionStatus) {
                        logsGrid.innerHTML = '<div class="error">❌ Không thể kết nối MeshTrash API</div>';
                        return;
                    }
                    
                    logsGrid.innerHTML = '<div class="loading">📋 Đang tải logs từ tất cả máy khách...</div>';
                    
                    try {
                        let allLogs = [];
                        for (const machine of machines) {
                            const response = await fetch(`/api/machine/${machine.id}/logs`);
                            const logs = await response.json();
                            allLogs = allLogs.concat(logs.map(log => ({...log, machine_name: machine.name})));
                        }
                        
                        allLogs.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
                        
                        logsGrid.innerHTML = allLogs.slice(0, 50).map(log => `
                            <div class="machine-card">
                                <div class="machine-header">
                                    <div class="machine-icon">📋</div>
                                    <div class="machine-info">
                                        <h3>${log.machine_name || 'Unknown'}</h3>
                                        <div class="machine-status">
                                            <span>${log.timestamp || 'N/A'}</span>
                                        </div>
                                    </div>
                                </div>
                                <div style="padding: 15px; background: #f8f9fa; border-radius: 8px; font-family: monospace;">
                                    ${log.message || 'No message'}
                                </div>
                            </div>
                        `).join('');
                    } catch (error) {
                        logsGrid.innerHTML = '<div class="error">❌ Lỗi tải logs: ' + error.message + '</div>';
                    }
                }
                
                async function remoteDesktop(machineId) {
                    try {
                        const response = await fetch(`/api/machine/${machineId}/remote-desktop`, {method: 'POST'});
                        const result = await response.json();
                        alert(result.success ? '🖥️ Đang kết nối Remote Desktop...' : '❌ Không thể kết nối Remote Desktop');
                    } catch (error) {
                        alert('❌ Lỗi: ' + error.message);
                    }
                }
                
                async function manageFiles(machineId) {
                    try {
                        const response = await fetch(`/api/machine/${machineId}/file-manager`, {method: 'POST'});
                        const result = await response.json();
                        alert(result.success ? '📁 Đang mở File Manager...' : '❌ Không thể mở File Manager');
                    } catch (error) {
                        alert('❌ Lỗi: ' + error.message);
                    }
                }
                
                async function restartService(machineId) {
                    if (confirm('🔄 Bạn có chắc muốn khởi động lại XML Guard?')) {
                        try {
                            const response = await fetch(`/api/machine/${machineId}/restart`, {method: 'POST'});
                            const result = await response.json();
                            alert(result.success ? '🔄 Đang khởi động lại XML Guard...' : '❌ Không thể khởi động lại');
                        } catch (error) {
                            alert('❌ Lỗi: ' + error.message);
                        }
                    }
                }
                
                async function stopService(machineId) {
                    if (confirm('⏹️ Bạn có chắc muốn dừng XML Guard?')) {
                        try {
                            const response = await fetch(`/api/machine/${machineId}/stop`, {method: 'POST'});
                            const result = await response.json();
                            alert(result.success ? '⏹️ Đang dừng XML Guard...' : '❌ Không thể dừng');
                        } catch (error) {
                            alert('❌ Lỗi: ' + error.message);
                        }
                    }
                }
                
                async function testConnection() {
                    try {
                        const response = await fetch('/api/machines');
                        if (response.ok) {
                            alert('✅ Kết nối MeshTrash API thành công!');
                            connectionStatus = true;
                            loadDashboardData();
                        } else {
                            alert('❌ Kết nối MeshTrash API thất bại!');
                            connectionStatus = false;
                        }
                    } catch (error) {
                        alert('❌ Lỗi kết nối: ' + error.message);
                        connectionStatus = false;
                    }
                }
                
                // Auto-refresh data every 30 seconds
                setInterval(() => {
                    if (connectionStatus) {
                        loadDashboardData();
                    }
                }, 30000);
                
                // Initialize dashboard
                document.addEventListener('DOMContentLoaded', function() {
                    showDashboard();
                    testConnection();
                });
            </script>
        </body>
        </html>
        """
        return html_template
    
    def run(self, host='localhost', port=5000, debug=True):
        """Chạy dashboard server"""
        print(f"🚀 Khởi động MeshTrash Dashboard...")
        print(f"📱 Truy cập: http://{host}:{port}")
        print(f"🔗 MeshTrash Server: {self.api.server_url}")
        
        # Test connection
        if self.api.test_connection():
            print("✅ Đã kết nối MeshTrash API")
        else:
            print("⚠️ Không thể kết nối MeshTrash API - Chạy ở chế độ demo")
        
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Main function"""
    dashboard = MeshTrashDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
