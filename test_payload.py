#!/usr/bin/env python3
"""
PyRai Advanced Test Payload - Enhanced Security Testing Version
ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.

This payload demonstrates advanced post-exploitation capabilities for authorized
penetration testing while maintaining safety through self-destruct mechanisms.
"""

import os
import sys
import time
import json
import socket
import platform
import subprocess
import threading
from datetime import datetime, timedelta

# SAFETY CONFIGURATION
TESTING_MODE = True
SELF_DESTRUCT_TIMER = 300  # 5 minutes
MAX_RUNTIME = 600  # 10 minutes maximum
AUTHORIZED_NETWORKS = ["192.0.2.0/24", "127.0.0.0/8"]  # Test networks only

class PayloadSafeguards:
    """Safety mechanisms to prevent misuse"""
    
    @staticmethod
    def validate_environment():
        """Validate we're in an authorized testing environment"""
        if not TESTING_MODE:
            return False
        
        # Check if we're in a controlled environment
        hostname = socket.gethostname().lower()
        test_indicators = ['test', 'lab', 'vm', 'sandbox', 'demo']
        
        if any(indicator in hostname for indicator in test_indicators):
            return True
            
        # Additional safety checks
        if os.path.exists('/tmp/pyrai_authorized'):
            return True
            
        return False
    
    @staticmethod
    def create_authorization_marker():
        """Create a marker file to indicate authorized testing"""
        try:
            marker_path = '/tmp/pyrai_authorized' if os.name != 'nt' else 'C:\\temp\\pyrai_authorized'
            os.makedirs(os.path.dirname(marker_path), exist_ok=True)
            with open(marker_path, 'w') as f:
                f.write(f"PyRai authorized testing session: {datetime.now()}\n")
            return True
        except:
            return False

class SystemRecon:
    """System reconnaissance module"""
    
    def __init__(self):
        self.info = {}
        
    def gather_system_info(self):
        """Gather comprehensive system information"""
        try:
            self.info = {
                'timestamp': datetime.now().isoformat(),
                'hostname': socket.gethostname(),
                'platform': platform.platform(),
                'architecture': platform.architecture(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'current_user': os.getenv('USER') or os.getenv('USERNAME'),
                'home_directory': os.path.expanduser('~'),
                'current_directory': os.getcwd(),
                'pid': os.getpid(),
                'ppid': os.getppid() if hasattr(os, 'getppid') else 'N/A'
            }
            
            # Network information
            self.info['ip_addresses'] = self._get_ip_addresses()
            
            # Environment variables (filtered for security)
            self.info['env_vars'] = self._get_safe_env_vars()
            
            # Running processes (if accessible)
            self.info['processes'] = self._get_process_list()
            
            return self.info
            
        except Exception as e:
            return {'error': f'System info gathering failed: {str(e)}'}
    
    def _get_ip_addresses(self):
        """Get system IP addresses"""
        try:
            addresses = []
            hostname = socket.gethostname()
            addresses.append(socket.gethostbyname(hostname))
            return addresses
        except:
            return ['Unable to determine']
    
    def _get_safe_env_vars(self):
        """Get filtered environment variables"""
        safe_vars = ['PATH', 'HOME', 'USER', 'SHELL', 'TERM', 'PWD']
        return {var: os.getenv(var, 'Not set') for var in safe_vars}
    
    def _get_process_list(self):
        """Get running processes (limited for safety)"""
        try:
            if os.name == 'nt':
                result = subprocess.run(['tasklist', '/fo', 'csv'], 
                                      capture_output=True, text=True, timeout=5)
            else:
                result = subprocess.run(['ps', 'aux'], 
                                      capture_output=True, text=True, timeout=5)
            
            # Return only first 10 lines for safety
            lines = result.stdout.split('\n')[:10]
            return lines
            
        except:
            return ['Process enumeration not available']

class NetworkDiscovery:
    """Network discovery and reconnaissance"""
    
    def __init__(self):
        self.discoveries = {}
    
    def scan_local_network(self):
        """Scan local network for active hosts (limited scope)"""
        try:
            # Only scan test network ranges
            if not TESTING_MODE:
                return {'error': 'Network scanning disabled outside testing mode'}
            
            active_hosts = []
            test_range = "192.0.2."  # RFC 3927 test range
            
            # Limited scan for testing
            for i in range(1, 5):  # Only scan first 4 IPs
                ip = f"{test_range}{i}"
                if self._ping_host(ip):
                    active_hosts.append(ip)
            
            self.discoveries['active_hosts'] = active_hosts
            self.discoveries['scan_range'] = f"{test_range}1-4"
            
            return self.discoveries
            
        except Exception as e:
            return {'error': f'Network discovery failed: {str(e)}'}
    
    def _ping_host(self, ip):
        """Ping a single host"""
        try:
            if os.name == 'nt':
                result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], 
                                      capture_output=True, timeout=3)
            else:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                      capture_output=True, timeout=3)
            
            return result.returncode == 0
        except:
            return False

class PersistenceDemo:
    """Demonstrate persistence mechanisms (safely)"""
    
    def __init__(self):
        self.persistence_methods = []
    
    def demonstrate_persistence(self):
        """Show persistence techniques without actually persisting"""
        techniques = {
            'cron_job': self._demo_cron_persistence,
            'startup_script': self._demo_startup_persistence,
            'service_creation': self._demo_service_persistence
        }
        
        results = {}
        for name, method in techniques.items():
            try:
                results[name] = method()
            except Exception as e:
                results[name] = f"Demo failed: {str(e)}"
        
        return results
    
    def _demo_cron_persistence(self):
        """Demonstrate cron-based persistence (simulation only)"""
        cron_entry = f"*/5 * * * * python3 /tmp/persistence_demo.py"
        return {
            'method': 'Cron job persistence',
            'entry': cron_entry,
            'location': '/etc/crontab or user crontab',
            'status': 'SIMULATED ONLY - Not actually created'
        }
    
    def _demo_startup_persistence(self):
        """Demonstrate startup script persistence (simulation only)"""
        if os.name == 'nt':
            location = 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'
            command = 'python3 C:\\temp\\persistence_demo.py'
        else:
            location = '/etc/init.d/ or ~/.bashrc'
            command = 'python3 /tmp/persistence_demo.py &'
        
        return {
            'method': 'Startup script persistence',
            'location': location,
            'command': command,
            'status': 'SIMULATED ONLY - Not actually created'
        }
    
    def _demo_service_persistence(self):
        """Demonstrate service-based persistence (simulation only)"""
        return {
            'method': 'System service persistence',
            'service_name': 'pyrai-demo-service',
            'status': 'SIMULATED ONLY - Not actually created',
            'description': 'Would create a system service for persistence'
        }

class CommunicationDemo:
    """Demonstrate C2 communication (safely)"""
    
    def __init__(self):
        self.c2_server = "127.0.0.1"  # Localhost only
        self.c2_port = 31339
    
    def demonstrate_c2(self):
        """Show C2 communication techniques"""
        methods = {
            'http_beacon': self._demo_http_beacon,
            'dns_tunnel': self._demo_dns_tunnel,
            'encrypted_channel': self._demo_encrypted_channel
        }
        
        results = {}
        for name, method in methods.items():
            try:
                results[name] = method()
            except Exception as e:
                results[name] = f"Demo failed: {str(e)}"
        
        return results
    
    def _demo_http_beacon(self):
        """Demonstrate HTTP beacon (simulation)"""
        return {
            'method': 'HTTP Beacon',
            'url': f'http://{self.c2_server}:{self.c2_port}/beacon',
            'frequency': '30 seconds',
            'status': 'SIMULATED ONLY - No actual communication'
        }
    
    def _demo_dns_tunnel(self):
        """Demonstrate DNS tunneling (simulation)"""
        return {
            'method': 'DNS Tunneling',
            'domain': 'test.local',
            'technique': 'TXT record exfiltration',
            'status': 'SIMULATED ONLY - No actual communication'
        }
    
    def _demo_encrypted_channel(self):
        """Demonstrate encrypted communication (simulation)"""
        return {
            'method': 'Encrypted Channel',
            'encryption': 'AES-256-GCM',
            'key_exchange': 'ECDH',
            'status': 'SIMULATED ONLY - No actual communication'
        }

class SelfDestruct:
    """Self-destruct mechanism"""
    
    def __init__(self, timer_seconds=300):
        self.timer = timer_seconds
        self.start_time = datetime.now()
        self.active = True
        
    def start_timer(self):
        """Start the self-destruct timer"""
        def countdown():
            time.sleep(self.timer)
            if self.active:
                self.execute_destruct()
        
        timer_thread = threading.Thread(target=countdown, daemon=True)
        timer_thread.start()
        
    def execute_destruct(self):
        """Execute self-destruct sequence"""
        try:
            print("\n" + "="*50)
            print("SELF-DESTRUCT SEQUENCE INITIATED")
            print("="*50)
            
            # Remove payload file
            try:
                os.remove(__file__)
                print(f"✓ Payload file {__file__} removed")
            except:
                print(f"✗ Could not remove {__file__}")
            
            # Remove test files
            test_files = [
                '/tmp/pyrai_test.txt',
                '/tmp/pyrai_authorized',
                '/tmp/pyrai_recon.json'
            ]
            
            if os.name == 'nt':
                test_files.extend([
                    'C:\\temp\\pyrai_test.txt',
                    'C:\\temp\\pyrai_authorized',
                    'C:\\temp\\pyrai_recon.json'
                ])
            
            for file_path in test_files:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"✓ Cleaned up {file_path}")
                except:
                    pass
            
            print("✓ Self-destruct completed successfully")
            print("="*50)
            
        except Exception as e:
            print(f"Self-destruct error: {str(e)}")
        
        finally:
            sys.exit(0)

def main():
    """Main payload execution"""
    print("="*60)
    print("PyRai Advanced Test Payload - Enhanced Security Testing")
    print("ETHICAL DISCLAIMER: This tool is for authorized testing only.")
    print("="*60)
    
    # Initialize safety mechanisms
    safeguards = PayloadSafeguards()
    
    # Validate environment
    if not safeguards.validate_environment():
        print("❌ SAFETY CHECK FAILED: Not in authorized testing environment")
        print("Creating authorization marker for testing...")
        if not safeguards.create_authorization_marker():
            print("❌ Could not create authorization marker. Exiting.")
            sys.exit(1)
    
    print("✅ Safety checks passed - Authorized testing environment detected")
    
    # Initialize self-destruct
    destroyer = SelfDestruct(SELF_DESTRUCT_TIMER)
    destroyer.start_timer()
    
    print(f"⏰ Self-destruct timer set for {SELF_DESTRUCT_TIMER} seconds")
    print(f"🕒 Execution started at: {datetime.now()}")
    
    # Create results dictionary
    results = {
        'payload_info': {
            'name': 'PyRai Advanced Test Payload',
            'version': '2.0',
            'execution_time': datetime.now().isoformat(),
            'testing_mode': TESTING_MODE,
            'self_destruct_timer': SELF_DESTRUCT_TIMER
        }
    }
    
    try:
        # System Reconnaissance
        print("\n🔍 Phase 1: System Reconnaissance")
        recon = SystemRecon()
        results['system_info'] = recon.gather_system_info()
        print(f"✓ Gathered system information for {results['system_info'].get('hostname', 'unknown')}")
        
        # Network Discovery
        print("\n🌐 Phase 2: Network Discovery")
        network = NetworkDiscovery()
        results['network_discovery'] = network.scan_local_network()
        print(f"✓ Network scan completed")
        
        # Persistence Demonstration
        print("\n🔄 Phase 3: Persistence Techniques (Demonstration)")
        persistence = PersistenceDemo()
        results['persistence_demo'] = persistence.demonstrate_persistence()
        print("✓ Persistence techniques demonstrated (simulated only)")
        
        # C2 Communication Demonstration
        print("\n📡 Phase 4: C2 Communication (Demonstration)")
        c2_demo = CommunicationDemo()
        results['c2_demo'] = c2_demo.demonstrate_c2()
        print("✓ C2 communication techniques demonstrated (simulated only)")
        
        # Save results
        results_file = '/tmp/pyrai_recon.json' if os.name != 'nt' else 'C:\\temp\\pyrai_recon.json'
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        # Display summary
        print("\n📊 EXECUTION SUMMARY")
        print("="*40)
        print(f"Hostname: {results['system_info'].get('hostname', 'Unknown')}")
        print(f"Platform: {results['system_info'].get('platform', 'Unknown')}")
        print(f"Current User: {results['system_info'].get('current_user', 'Unknown')}")
        print(f"Active Hosts Found: {len(results['network_discovery'].get('active_hosts', []))}")
        print(f"Persistence Methods: {len(results['persistence_demo'])}")
        print(f"C2 Methods: {len(results['c2_demo'])}")
        
        print(f"\n⚠️  WARNING: This was a demonstration payload")
        print(f"⚠️  All techniques were simulated for testing purposes")
        print(f"⚠️  Self-destruct will activate in {SELF_DESTRUCT_TIMER} seconds")
        
        # Wait before self-destruct
        print(f"\n⏳ Payload execution completed. Waiting for self-destruct...")
        time.sleep(10)  # Wait 10 seconds before manual cleanup
        
    except Exception as e:
        print(f"\n❌ Payload execution error: {str(e)}")
        results['error'] = str(e)
    
    finally:
        # Manual cleanup if still running
        if destroyer.active:
            print("\n🧹 Initiating manual cleanup...")
            destroyer.execute_destruct()

if __name__ == "__main__":
    main() 