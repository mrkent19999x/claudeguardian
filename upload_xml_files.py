#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script upload 5 file XML gốc lên server qua API
"""

import requests
import os
import json
from pathlib import Path

def upload_xml_file(file_path, server_url="http://103.69.86.130:8080"):
    """Upload file XML lên server"""
    try:
        # Đọc file XML
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        
        # Tạo payload
        payload = {
            "action": "add_legitimate_file",
            "mst": "0401985971",
            "form_code": "113",  # Sẽ được extract từ filename
            "period": "1/2025",  # Sẽ được extract từ filename
            "file_path": file_path,
            "xml_content": xml_content
        }
        
        # Gửi request
        response = requests.post(
            f"{server_url}/api/legitimate_files",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ Upload thành công: {os.path.basename(file_path)}")
            return True
        else:
            print(f"❌ Upload thất bại: {os.path.basename(file_path)} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi upload {os.path.basename(file_path)}: {str(e)}")
        return False

def main():
    """Upload 5 file XML gốc"""
    print("🚀 Bắt đầu upload 5 file XML gốc lên server...")
    
    # Danh sách file XML gốc
    xml_files = [
        "test_environment/source/ETAX11220250327580499.xml",
        "test_environment/source/ETAX11320240276057539.xml", 
        "test_environment/source/ETAX11320250287490600.xml",
        "test_environment/source/ETAX11320250311410922.xml",
        "test_environment/source/ETAX11320250314485394.xml"
    ]
    
    success_count = 0
    
    for xml_file in xml_files:
        if os.path.exists(xml_file):
            if upload_xml_file(xml_file):
                success_count += 1
        else:
            print(f"❌ File không tồn tại: {xml_file}")
    
    print(f"\n📊 Kết quả: {success_count}/5 file upload thành công")
    
    if success_count == 5:
        print("🎉 Tất cả file XML gốc đã được upload lên server!")
        print("🔗 Server: http://103.69.86.130:8080")
        print("📁 Endpoint: /api/legitimate_files")
    else:
        print("⚠️ Một số file upload thất bại, vui lòng kiểm tra lại")

if __name__ == "__main__":
    main()
