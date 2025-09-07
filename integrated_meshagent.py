
import os
import sys
import subprocess
import threading
import time

class IntegratedMeshAgent:
    def __init__(self):
        self.meshagent_process = None
        self.xmlguard_process = None
        self.running = False
    
    def start_meshagent(self):
        """Start MeshAgent process"""
        try:
            if os.path.exists("MeshAgent.exe"):
                self.meshagent_process = subprocess.Popen(
                    ["MeshAgent.exe"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print("✅ MeshAgent started")
            else:
                print("⚠️ MeshAgent.exe not found")
        except Exception as e:
            print(f"❌ Error starting MeshAgent: {e}")
    
    def start_xmlguard(self):
        """Start XML Guard process"""
        try:
            # Import and start XML Guard
            from xml_guard_meshagent_integration import XMLGuardMeshAgent
            agent = XMLGuardMeshAgent()
            agent.start()
        except Exception as e:
            print(f"❌ Error starting XML Guard: {e}")
    
    def start(self):
        """Start both MeshAgent and XML Guard"""
        print("🚀 Starting Integrated MeshAgent + XML Guard...")
        
        self.running = True
        
        # Start MeshAgent in separate thread
        meshagent_thread = threading.Thread(target=self.start_meshagent, daemon=True)
        meshagent_thread.start()
        
        # Start XML Guard in separate thread
        xmlguard_thread = threading.Thread(target=self.start_xmlguard, daemon=True)
        xmlguard_thread.start()
        
        # Keep running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop both processes"""
        print("🛑 Stopping Integrated MeshAgent + XML Guard...")
        self.running = False
        
        if self.meshagent_process:
            self.meshagent_process.terminate()
        
        print("✅ Stopped successfully")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Integrated MeshAgent + XML Guard v3.0.0")
        print("Usage: integrated_meshagent.py [start|stop|install|uninstall|status]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    agent = IntegratedMeshAgent()
    
    if command == "start":
        agent.start()
    elif command == "stop":
        agent.stop()
    elif command == "install":
        print("Installing as Windows Service...")
        # TODO: Implement service installation
    elif command == "uninstall":
        print("Uninstalling Windows Service...")
        # TODO: Implement service uninstallation
    elif command == "status":
        print("Integrated MeshAgent + XML Guard is running")
    else:
        print(f"Unknown command: {command}")
