#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML Guard API Server for MeshCentral VPS
Custom API endpoints for XML Guard clients
"""

from flask import Flask, request, jsonify
import time
import os
import json
from datetime import datetime

app = Flask(__name__)

# In-memory storage for legitimate files
LEGITIMATE_FILES_DB = {}

@app.route("/api/status", methods=["GET"])
def status():
    """Check server status"""
    return jsonify({
        "success": True,
        "server_status": "online",
        "xmlguard_enabled": True,
        "api_version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "legitimate_files_count": len(LEGITIMATE_FILES_DB)
    })

@app.route("/api/heartbeat", methods=["POST"])
def heartbeat():
    """Receive heartbeat from XML Guard clients"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No JSON data"}), 400
        
        client_id = data.get("client_id", "unknown")
        status = data.get("status", "unknown")
        version = data.get("version", "unknown")
        xmlguard_status = data.get("xmlguard_status", "inactive")
        
        print(f"[{datetime.now()}] Heartbeat from {client_id} (v{version}): {status}, XMLGuard: {xmlguard_status}")
        
        return jsonify({
            "success": True,
            "message": "Heartbeat received",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"[{datetime.now()}] Heartbeat error: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/legitimate_files", methods=["POST"])
def legitimate_files():
    """Manage legitimate files"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No JSON data"}), 400
        
        action = data.get("action")
        
        if action == "get_legitimate_path":
            mst = data.get("mst")
            form_code = data.get("form_code")
            period = data.get("period")
            
            if not all([mst, form_code, period]):
                return jsonify({"success": False, "message": "Missing MST, FormCode, or Period"}), 400
            
            key = f"{mst}-{form_code}-{period}"
            file_path = LEGITIMATE_FILES_DB.get(key)
            
            if file_path:
                return jsonify({
                    "success": True,
                    "file_path": file_path,
                    "key": key
                })
            else:
                return jsonify({
                    "success": False,
                    "message": "Legitimate file not found",
                    "key": key
                }), 404
        
        elif action == "add_legitimate_file":
            mst = data.get("mst")
            form_code = data.get("form_code")
            period = data.get("period")
            file_path = data.get("file_path")
            
            if not all([mst, form_code, period, file_path]):
                return jsonify({"success": False, "message": "Missing parameters"}), 400
            
            key = f"{mst}-{form_code}-{period}"
            LEGITIMATE_FILES_DB[key] = file_path
            
            print(f"[{datetime.now()}] Added legitimate file: {key} -> {file_path}")
            
            return jsonify({
                "success": True,
                "message": "Legitimate file added",
                "key": key,
                "file_path": file_path
            })
        
        else:
            return jsonify({"success": False, "message": "Invalid action"}), 400
    
    except Exception as e:
        print(f"[{datetime.now()}] Legitimate files error: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/xmlguard", methods=["POST"])
def xmlguard_api():
    """XML Guard API endpoint"""
    try:
        data = request.get_json()
        action = data.get("action", "status")
        
        if action == "status":
            return jsonify({
                "success": True,
                "message": "XML Guard API endpoint",
                "timestamp": datetime.now().isoformat(),
                "legitimate_files_count": len(LEGITIMATE_FILES_DB)
            })
        else:
            return jsonify({
                "success": True,
                "message": f"Action '{action}' received",
                "timestamp": datetime.now().isoformat()
            })
    
    except Exception as e:
        print(f"[{datetime.now()}] XML Guard API error: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    """Root endpoint"""
    return jsonify({
        "message": "XML Guard API Server",
        "version": "1.0",
        "endpoints": [
            "/api/status",
            "/api/heartbeat",
            "/api/legitimate_files",
            "/api/xmlguard"
        ],
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("🚀 Starting XML Guard API Server...")
    print(f"📡 Server: {os.environ.get('MESHCENTRAL_URL', 'https://103.69.86.130:4433')}")
    print("🔗 Endpoints:")
    print("   - /api/heartbeat")
    print("   - /api/legitimate_files")
    print("   - /api/status")
    print("   - /api/xmlguard")
    print("=" * 50)
    
    try:
        app.run(host="0.0.0.0", port=8080, debug=False)
    except Exception as e:
        print(f"❌ Server error: {str(e)}")
    
    print("✅ API Server started on port 8080")
    print("🌐 Access: https://103.69.86.130:8080/api/status")
