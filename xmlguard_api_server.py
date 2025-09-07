#!/usr/bin/env python3
"""
XML Guard API Server for MeshCentral VPS
Custom API endpoints for XML Guard clients
"""

import json
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class XMLGuardAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "server_status": "online",
                "xmlguard_enabled": True,
                "api_version": "1.0.0",
                "timestamp": datetime.now().isoformat(),
                "endpoints": ["/api/heartbeat", "/api/legitimate_files", "/api/status", "/api/xmlguard"]
            }
            
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        if self.path == "/api/heartbeat":
            self.handle_heartbeat(data)
        elif self.path == "/api/legitimate_files":
            self.handle_legitimate_files(data)
        elif self.path == "/api/xmlguard":
            self.handle_xmlguard(data)
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_heartbeat(self, data):
        """Handle heartbeat requests"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "success": True,
            "message": "Heartbeat received",
            "timestamp": datetime.now().isoformat(),
            "server_status": "online",
            "client_id": data.get("client_id", "unknown"),
            "version": data.get("version", "unknown")
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def handle_legitimate_files(self, data):
        """Handle legitimate files requests"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        mst = data.get("mst", "")
        form_code = data.get("form_code", "")
        period = data.get("period", "")
        action = data.get("action", "")
        
        if action == "get_legitimate_path":
            # Return path to legitimate file
            legitimate_path = f"C:/TaxFiles/Legitimate/ETAX{mst}_{form_code}_{period.replace('/', '_')}.xml"
            
            response = {
                "success": True,
                "file_path": legitimate_path,
                "mst": mst,
                "form_code": form_code,
                "period": period,
                "timestamp": datetime.now().isoformat()
            }
        else:
            response = {
                "success": False,
                "error": f"Unknown action: {action}"
            }
        
        self.wfile.write(json.dumps(response).encode())
    
    def handle_xmlguard(self, data):
        """Handle XML Guard specific requests"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        action = data.get("action", "")
        
        if action == "register_client":
            response = {
                "success": True,
                "client_id": data.get("client_id", "unknown"),
                "status": "registered",
                "timestamp": datetime.now().isoformat()
            }
        elif action == "get_config":
            response = {
                "success": True,
                "config": {
                    "check_interval": 30,
                    "max_memory_mb": 500,
                    "watch_paths": ["C:\\", "D:\\", "E:\\"],
                    "company_mst": "0401985971"
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            response = {
                "success": False,
                "error": f"Unknown action: {action}"
            }
        
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def main():
    """Start API server"""
    print("🚀 Starting XML Guard API Server...")
    print("📡 Server: https://103.69.86.130:4433")
    print("🔗 Endpoints:")
    print("   - /api/heartbeat")
    print("   - /api/legitimate_files") 
    print("   - /api/status")
    print("   - /api/xmlguard")
    print("=" * 50)
    
    # Start server on port 8080 (different from MeshCentral)
    server = HTTPServer(('0.0.0.0', 8080), XMLGuardAPIHandler)
    print("✅ API Server started on port 8080")
    print("🌐 Access: https://103.69.86.130:8080/api/status")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping API Server...")
        server.shutdown()

if __name__ == "__main__":
    main()
