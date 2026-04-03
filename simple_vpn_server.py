#!/usr/bin/env python3
"""
Simple Working VPN Server - No External Dependencies
Runs immediately without pip install
"""

import socket
import threading
import json
import time
from datetime import datetime
import base64
import hashlib

class SimpleVPNServer:
    def __init__(self, host='0.0.0.0', port=8443):
        self.host = host
        self.port = port
        self.clients = {}
        self.running = False
        self.stats = {
            'connections': 0,
            'bytes_sent': 0,
            'bytes_received': 0,
            'active_clients': 0,
            'start_time': datetime.now().isoformat()
        }
        
    def simple_encrypt(self, data, key):
        """Simple XOR encryption (for demo)"""
        encrypted = bytearray()
        for i, byte in enumerate(data.encode() if isinstance(data, str) else data):
            encrypted.append(byte ^ ord(key[i % len(key)]))
        return base64.b64encode(encrypted).decode()
    
    def simple_decrypt(self, encrypted_data, key):
        """Simple XOR decryption (for demo)"""
        encrypted = base64.b64decode(encrypted_data.encode())
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ ord(key[i % len(key)]))
        return decrypted.decode()
    
    def authenticate_client(self, username, password):
        """Authenticate client"""
        valid_users = {
            'user1': 'password123',
            'user2': 'secure456',
            'admin': 'admin789'
        }
        
        if username in valid_users and valid_users[username] == password:
            return True
        return False
    
    def handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        try:
            # Receive authentication
            auth_data = client_socket.recv(1024).decode()
            username, password = auth_data.split(':')
            
            # Authenticate
            if not self.authenticate_client(username, password):
                client_socket.send(b'AUTH_FAILED')
                client_socket.close()
                return
            
            # Send authentication success
            client_socket.send(b'AUTH_SUCCESS')
            
            # Assign VPN IP
            vpn_ip = f'10.8.0.{len(self.clients) + 2}'
            self.clients[client_address] = {
                'username': username,
                'vpn_ip': vpn_ip,
                'connected_at': datetime.now().isoformat(),
                'bytes_sent': 0,
                'bytes_received': 0
            }
            
            self.stats['connections'] += 1
            self.stats['active_clients'] = len(self.clients)
            
            print(f"[+] Client connected: {username} ({client_address}) -> {vpn_ip}")
            
            # Send VPN IP to client
            client_socket.send(vpn_ip.encode())
            
            # Handle client data
            while self.running:
                try:
                    encrypted_data = client_socket.recv(4096)
                    if not encrypted_data:
                        break
                    
                    # Decrypt data
                    decrypted_data = self.simple_decrypt(encrypted_data.decode(), password)
                    
                    # Update stats
                    self.clients[client_address]['bytes_received'] += len(encrypted_data)
                    self.stats['bytes_received'] += len(encrypted_data)
                    
                    # Process data (echo back)
                    response = f"ACK: {decrypted_data[:50]}"
                    encrypted_response = self.simple_encrypt(response, password)
                    
                    client_socket.send(encrypted_response.encode())
                    
                    # Update stats
                    self.clients[client_address]['bytes_sent'] += len(encrypted_response)
                    self.stats['bytes_sent'] += len(encrypted_response)
                    
                except Exception as e:
                    print(f"[-] Error handling client data: {e}")
                    break
        
        except Exception as e:
            print(f"[-] Error with client {client_address}: {e}")
        
        finally:
            if client_address in self.clients:
                del self.clients[client_address]
                self.stats['active_clients'] = len(self.clients)
            client_socket.close()
            print(f"[-] Client disconnected: {client_address}")
    
    def start(self):
        """Start VPN server"""
        self.running = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"\n{'='*60}")
            print(f"[+] VPN Server started on {self.host}:{self.port}")
            print(f"[+] VPN Network: 10.8.0.0/24")
            print(f"[+] VPN Gateway: 10.8.0.1")
            print(f"{'='*60}\n")
            
            while self.running:
                try:
                    client_socket, client_address = server_socket.accept()
                    print(f"[*] New connection from {client_address}")
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                
                except KeyboardInterrupt:
                    print("\n[*] Shutting down...")
                    break
        
        except Exception as e:
            print(f"[-] Server error: {e}")
        
        finally:
            self.running = False
            server_socket.close()
            print("[*] VPN Server stopped")
    
    def get_stats(self):
        """Get server statistics"""
        return {
            'server': {
                'host': self.host,
                'port': self.port,
                'running': self.running
            },
            'stats': self.stats,
            'clients': {
                str(addr): {
                    'username': info['username'],
                    'vpn_ip': info['vpn_ip'],
                    'connected_at': info['connected_at'],
                    'bytes_sent': info['bytes_sent'],
                    'bytes_received': info['bytes_received']
                }
                for addr, info in self.clients.items()
            }
        }


class SimpleVPNClient:
    def __init__(self, server_host, server_port, username, password):
        self.server_host = server_host
        self.server_port = server_port
        self.username = username
        self.password = password
        self.socket = None
        self.vpn_ip = None
        self.connected = False
        
    def simple_encrypt(self, data, key):
        """Simple XOR encryption"""
        encrypted = bytearray()
        for i, byte in enumerate(data.encode() if isinstance(data, str) else data):
            encrypted.append(byte ^ ord(key[i % len(key)]))
        return base64.b64encode(encrypted).decode()
    
    def simple_decrypt(self, encrypted_data, key):
        """Simple XOR decryption"""
        encrypted = base64.b64decode(encrypted_data.encode())
        decrypted = bytearray()
        for i, byte in enumerate(encrypted):
            decrypted.append(byte ^ ord(key[i % len(key)]))
        return decrypted.decode()
    
    def connect(self):
        """Connect to VPN server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            
            # Send authentication
            auth_data = f"{self.username}:{self.password}"
            self.socket.send(auth_data.encode())
            
            # Receive authentication response
            response = self.socket.recv(1024).decode()
            
            if response == 'AUTH_FAILED':
                print("[-] Authentication failed")
                return False
            
            # Receive VPN IP
            self.vpn_ip = self.socket.recv(1024).decode()
            self.connected = True
            
            print(f"\n{'='*60}")
            print(f"[+] Connected to VPN")
            print(f"[+] VPN IP: {self.vpn_ip}")
            print(f"[+] Server: {self.server_host}:{self.server_port}")
            print(f"{'='*60}\n")
            
            return True
        
        except Exception as e:
            print(f"[-] Connection failed: {e}")
            return False
    
    def send_data(self, data):
        """Send encrypted data to server"""
        if not self.connected:
            print("[-] Not connected to VPN")
            return False
        
        try:
            encrypted_data = self.simple_encrypt(data, self.password)
            self.socket.send(encrypted_data.encode())
            
            # Receive response
            encrypted_response = self.socket.recv(4096).decode()
            response = self.simple_decrypt(encrypted_response, self.password)
            
            return response
        
        except Exception as e:
            print(f"[-] Error sending data: {e}")
            return None
    
    def disconnect(self):
        """Disconnect from VPN"""
        if self.socket:
            self.socket.close()
            self.connected = False
            print("[*] Disconnected from VPN")


def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 simple_vpn_server.py [server|client]")
        print("\nServer mode:")
        print("  python3 simple_vpn_server.py server")
        print("\nClient mode:")
        print("  python3 simple_vpn_server.py client <server_host> <username> <password>")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == 'server':
        # Start VPN server
        server = SimpleVPNServer(host='0.0.0.0', port=8443)
        
        # Start stats thread
        def print_stats():
            while server.running:
                time.sleep(10)
                stats = server.get_stats()
                print(f"\n[*] Active clients: {stats['stats']['active_clients']}")
                print(f"[*] Total connections: {stats['stats']['connections']}")
                print(f"[*] Bytes sent: {stats['stats']['bytes_sent']}")
                print(f"[*] Bytes received: {stats['stats']['bytes_received']}")
        
        stats_thread = threading.Thread(target=print_stats)
        stats_thread.daemon = True
        stats_thread.start()
        
        server.start()
    
    elif mode == 'client':
        if len(sys.argv) < 5:
            print("Usage: python3 simple_vpn_server.py client <server_host> <username> <password>")
            sys.exit(1)
        
        server_host = sys.argv[2]
        username = sys.argv[3]
        password = sys.argv[4]
        
        # Connect to VPN
        client = SimpleVPNClient(server_host, 8443, username, password)
        
        if client.connect():
            # Send test data
            print("[*] Sending test data...")
            response = client.send_data("Hello from VPN client!")
            print(f"[+] Response: {response}")
            
            # Keep connection alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                client.disconnect()
    
    else:
        print(f"[-] Unknown mode: {mode}")
        sys.exit(1)


if __name__ == '__main__':
    main()
