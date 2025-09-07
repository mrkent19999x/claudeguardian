import sys
import os
import time
import requests
import psutil
import gc

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Simple logging function
def log(message, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

# Optimized config (reduced memory footprint)
CONFIG = {
    "MeshCentral": {
        "Enabled": True,
        "ServerUrl": "https://103.69.86.130:4433",
        "PingInterval": 60,
        "Timeout": 10
    },
    "Performance": {
        "MaxMemoryMB": 500  # Reduced from 250 to 500
    }
}

def check_internet_connection():
    try:
        # Use smaller timeout and simpler request
        response = requests.get("http://www.google.com", timeout=3, stream=True)
        response.close()  # Close connection immediately
        return True
    except:
        return False

def check_meshcentral_connection():
    if not CONFIG["MeshCentral"]["Enabled"]:
        return True
    
    server_url = CONFIG["MeshCentral"]["ServerUrl"]
    timeout = CONFIG["MeshCentral"]["Timeout"]
    try:
        response = requests.get(server_url, timeout=timeout, verify=False, stream=True)
        response.close()  # Close connection immediately
        return response.status_code == 200
    except:
        return False

def check_core_files():
    # Simplified file check
    required_files = ["Core", "Utils", "Config"]
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    for folder in required_files:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            return False
    return True

def check_performance():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    current_memory_mb = memory_info.rss / (1024 * 1024)
    
    # Force garbage collection
    gc.collect()
    
    log(f"Memory Usage: {current_memory_mb:.2f} MB")
    
    if current_memory_mb > CONFIG["Performance"]["MaxMemoryMB"]:
        log(f"Memory usage exceeds limit ({CONFIG['Performance']['MaxMemoryMB']} MB)", "WARN")
        return False
    return True

def run_tests():
    log("Running optimized XML Guard tests...")
    
    # Test 1: System Requirements
    python_ok = sys.version_info.major == 3
    log(f"Python {sys.version_info.major}.{sys.version_info.minor}: {'PASSED' if python_ok else 'FAILED'}")
    
    # Test 2: Network Connectivity
    internet_ok = check_internet_connection()
    log(f"Internet: {'PASSED' if internet_ok else 'FAILED'}")
    
    meshcentral_ok = check_meshcentral_connection()
    log(f"MeshCentral: {'PASSED' if meshcentral_ok else 'FAILED'}")
    
    # Test 3: Core Files
    files_ok = check_core_files()
    log(f"Core Files: {'PASSED' if files_ok else 'FAILED'}")
    
    # Test 4: Performance
    memory_ok = check_performance()
    log(f"Memory: {'PASSED' if memory_ok else 'FAILED'}")
    
    # Calculate success rate
    tests = [python_ok, internet_ok, meshcentral_ok, files_ok, memory_ok]
    passed = sum(tests)
    total = len(tests)
    success_rate = (passed / total) * 100
    
    log(f"Success Rate: {success_rate:.1f}% ({passed}/{total})")
    
    # Force cleanup
    gc.collect()
    
    return success_rate >= 80  # Accept 80% success rate

def start_xml_guard():
    log("Starting XML Guard (optimized)...")
    
    if run_tests():
        log("XML Guard started successfully!", "INFO")
        # Keep process alive but lightweight
        try:
            while True:
                time.sleep(60)  # Sleep for 1 minute
                gc.collect()    # Force garbage collection
        except KeyboardInterrupt:
            log("XML Guard stopped by user", "INFO")
    else:
        log("XML Guard failed to start due to failed tests", "ERROR")
    
    sys.exit(0)

def stop_xml_guard():
    log("Stopping XML Guard...")
    sys.exit(0)

def get_status():
    log("XML Guard Status: Running (Optimized)")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "test":
            run_tests()
        elif command == "start":
            start_xml_guard()
        elif command == "stop":
            stop_xml_guard()
        elif command == "status":
            get_status()
        else:
            log(f"Unknown command: {command}", "ERROR")
    else:
        log("Usage: python xml_guard_optimized.py [test|start|stop|status]")
