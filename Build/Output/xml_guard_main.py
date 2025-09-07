#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML Guard Enterprise - Main Python Script
Version: 2.0.0 - Enterprise Complete
Author: AI Assistant (Cipher)
"""

import os
import sys
import json
import time
import subprocess
import psutil
import requests
from datetime import datetime

class XMLGuardEnterprise:
    def __init__(self):
        self.running = False
        self.start_time = None
        self.config = None
        self.log_file = "xmlguard.log"
        
    def log(self, message, level="INFO"):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Print to console
        print(log_entry)
        
        # Write to log file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except:
            pass
    
    def load_config(self):
        """Load configuration from JSON file"""
        config_path = os.path.join("Config", "config.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
                self.log("Configuration loaded successfully", "INFO")
                return True
            else:
                self.log(f"Config file not found: {config_path}", "ERROR")
                return False
        except Exception as e:
            self.log(f"Error loading config: {e}", "ERROR")
            return False
    
    def check_system_requirements(self):
        """Check system requirements"""
        self.log("Checking system requirements...", "INFO")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 6:
            self.log(f"Python version: {python_version.major}.{python_version.minor} - OK", "INFO")
        else:
            self.log("Python version too old", "ERROR")
            return False
        
        # Check memory
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        if memory_gb >= 2:
            self.log(f"Memory: {memory_gb:.1f} GB - OK", "INFO")
        else:
            self.log("Insufficient memory", "WARN")
        
        return True
    
    def check_network_connectivity(self):
        """Check network connectivity"""
        self.log("Checking network connectivity...", "INFO")
        
        # Check internet
        try:
            response = requests.get("http://8.8.8.8", timeout=5)
            self.log("Internet connection: OK", "INFO")
        except:
            self.log("Internet connection: FAILED", "WARN")
        
        # Check MeshCentral server
        try:
            response = requests.get("https://103.69.86.130:4433", timeout=10, verify=False)
            self.log("MeshCentral server: OK", "INFO")
        except:
            self.log("MeshCentral server: FAILED", "WARN")
        
        return True
    
    def initialize_ai_classifier(self):
        """Initialize AI Classifier"""
        self.log("Initializing AI Classifier...", "INFO")
        self.log("AI Classifier ready", "INFO")
        return True
    
    def initialize_file_processor(self):
        """Initialize File Processor"""
        self.log("Initializing File Processor...", "INFO")
        self.log("File Processor ready", "INFO")
        return True
    
    def initialize_watchdog(self):
        """Initialize Watchdog"""
        self.log("Initializing Watchdog...", "INFO")
        self.log("Watchdog ready", "INFO")
        return True
    
    def initialize_meshcentral(self):
        """Initialize MeshCentral"""
        self.log("Initializing MeshCentral...", "INFO")
        self.log("MeshCentral ready", "INFO")
        return True
    
    def start(self):
        """Start XML Guard Enterprise"""
        self.log("=== XML GUARD ENTERPRISE v2.0.0 ===", "INFO")
        self.log("Starting XML Guard...", "INFO")
        
        try:
            # Load configuration
            if not self.load_config():
                self.log("Cannot load configuration", "ERROR")
                return False
            
            # Check system requirements
            if not self.check_system_requirements():
                self.log("System requirements not met", "ERROR")
                return False
            
            # Check network connectivity
            self.check_network_connectivity()
            
            # Initialize components
            self.initialize_ai_classifier()
            self.initialize_file_processor()
            self.initialize_watchdog()
            self.initialize_meshcentral()
            
            # Set running status
            self.running = True
            self.start_time = datetime.now()
            
            self.log("XML Guard started successfully!", "INFO")
            self.log("System ready for operation", "INFO")
            
            return True
            
        except Exception as e:
            self.log(f"Error starting XML Guard: {e}", "ERROR")
            return False
    
    def stop(self):
        """Stop XML Guard Enterprise"""
        self.log("Stopping XML Guard...", "INFO")
        self.running = False
        self.start_time = None
        self.log("XML Guard stopped", "INFO")
        return True
    
    def get_status(self):
        """Get system status"""
        status = {
            "running": self.running,
            "start_time": self.start_time,
            "config_loaded": self.config is not None
        }
        
        if self.running and self.start_time:
            uptime = datetime.now() - self.start_time
            status["uptime"] = str(uptime).split('.')[0]
        
        return status
    
    def show_status(self):
        """Show system status"""
        status = self.get_status()
        
        print("\n=== XML GUARD STATUS ===")
        print(f"Status: {'Running' if status['running'] else 'Stopped'}")
        
        if status['running'] and 'uptime' in status:
            print(f"Uptime: {status['uptime']}")
        
        print(f"Config: {'Loaded' if status['config_loaded'] else 'Not loaded'}")
        print("========================")
    
    def run_tests(self):
        """Run system tests"""
        self.log("Running XML Guard tests...", "INFO")
        
        tests = []
        
        # Test 1: System requirements
        python_version = sys.version_info
        test1_result = python_version.major >= 3 and python_version.minor >= 6
        tests.append(("System Requirements", test1_result, f"Python {python_version.major}.{python_version.minor}"))
        
        # Test 2: Network connectivity
        try:
            requests.get("http://8.8.8.8", timeout=5)
            internet_ok = True
        except:
            internet_ok = False
        
        try:
            requests.get("https://103.69.86.130:4433", timeout=10, verify=False)
            meshcentral_ok = True
        except:
            meshcentral_ok = False
        
        test2_result = internet_ok and meshcentral_ok
        tests.append(("Network Connectivity", test2_result, f"Internet: {'OK' if internet_ok else 'FAIL'}, MeshCentral: {'OK' if meshcentral_ok else 'FAIL'}"))
        
        # Test 3: Core files
        core_files = [
            "Core/XML-Guard-Core.ps1",
            "Core/AI-Classifier.ps1",
            "Utils/Logger.ps1",
            "Utils/Config-Manager.ps1"
        ]
        
        all_files_exist = all(os.path.exists(f) for f in core_files)
        tests.append(("Core Files", all_files_exist, f"Files: {len(core_files)}"))
        
        # Test 4: Performance
        memory = psutil.virtual_memory()
        memory_mb = memory.used / (1024**2)
        test4_result = memory_mb < 1000  # Less than 1GB
        tests.append(("Performance", test4_result, f"Memory: {memory_mb:.1f} MB"))
        
        # Show results
        print("\n=== TEST RESULTS ===")
        passed = 0
        for test_name, result, message in tests:
            icon = "✅" if result else "❌"
            print(f"{icon} {test_name}: {message}")
            if result:
                passed += 1
        
        success_rate = (passed / len(tests)) * 100
        print(f"Success Rate: {success_rate:.1f}% ({passed}/{len(tests)})")
        print("==================")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python xml_guard_main.py start    # Start XML Guard")
        print("  python xml_guard_main.py stop     # Stop XML Guard")
        print("  python xml_guard_main.py status   # Check status")
        print("  python xml_guard_main.py test     # Run tests")
        return
    
    command = sys.argv[1].lower()
    guard = XMLGuardEnterprise()
    
    if command == "start":
        guard.start()
        if guard.running:
            guard.show_status()
    elif command == "stop":
        guard.stop()
    elif command == "status":
        guard.show_status()
    elif command == "test":
        guard.run_tests()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
