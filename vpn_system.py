#!/usr/bin/env python3
"""
Real VPN System - Demonstrates encryption, tunneling, and performance measurement
"""

import socket
import threading
import time
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
from datetime import datetime

class VPNTunnel:
    """Real VPN tunnel with encryption"""
    
    def __init__(self, server_port=5555):
        self.server_port = server_port
        self.running = False
        self.stats = {
            'packets_sent': 0,
            'packets_received': 0,
            'bytes_encrypted': 0,
            'bytes_decrypted': 0,
            'encryption_time_ms': 0
        }
        self.encryption_key = self._generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.server_socket = None
        self.client_socket = None
        
    def _generate_key(self):
        """Generate encryption key"""
        password = b"vpn_secure_tunnel_2025"
        salt = b"vpn_salt_12345678"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt_packet(self, data):
        """Encrypt packet"""
        start = time.time()
        encrypted = self.cipher.encrypt(data)
        elapsed = (time.time() - start) * 1000
        self.stats['bytes_encrypted'] += len(data)
        self.stats['encryption_time_ms'] += elapsed
        return encrypted
    
    def decrypt_packet(self, encrypted_data):
        """Decrypt packet"""
        start = time.time()
        decrypted = self.cipher.decrypt(encrypted_data)
        elapsed = (time.time() - start) * 1000
        self.stats['bytes_decrypted'] += len(decrypted)
        self.stats['encryption_time_ms'] += elapsed
        return decrypted
    
    def start_server(self):
        """Start VPN server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('127.0.0.1', self.server_port))
        self.server_socket.listen(1)
        self.running = True
        
        try:
            conn, addr = self.server_socket.accept()
            encrypted_data = conn.recv(65536)
            if encrypted_data:
                decrypted = self.decrypt_packet(encrypted_data)
                self.stats['packets_received'] += 1
                response = self.encrypt_packet(decrypted)
                self.stats['packets_sent'] += 1
                conn.send(response)
            conn.close()
        except Exception as e:
            pass
        finally:
            self.running = False
            if self.server_socket:
                self.server_socket.close()
    
    def send_data(self, data):
        """Send data through VPN tunnel"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('127.0.0.1', self.server_port))
            
            encrypted = self.encrypt_packet(data)
            self.stats['packets_sent'] += 1
            self.client_socket.send(encrypted)
            
            response = self.client_socket.recv(65536)
            decrypted = self.decrypt_packet(response)
            self.stats['packets_received'] += 1
            
            return decrypted
        except Exception as e:
            return None
        finally:
            if self.client_socket:
                self.client_socket.close()


class VPNPerformanceTester:
    """Test VPN performance"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.results = []
    
    def read_file(self):
        """Read test file"""
        with open(self.file_path, 'rb') as f:
            return f.read()
    
    def test_baseline(self, trials=5):
        """Test baseline (no VPN)"""
        print("\n" + "="*60)
        print("BASELINE TEST (No VPN)")
        print("="*60)
        
        data = self.read_file()
        times = []
        
        for i in range(trials):
            start = time.time()
            _ = hashlib.sha256(data).hexdigest()
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"Trial {i+1}: {elapsed:.4f}s")
        
        avg_time = sum(times) / len(times) if times else 0.001
        throughput = (len(data) / avg_time) / 1024 if avg_time > 0 else 0
        
        result = {
            'type': 'baseline',
            'avg_time': avg_time,
            'throughput_kbps': throughput,
            'file_size_kb': len(data) / 1024
        }
        self.results.append(result)
        
        print(f"\nBaseline Average: {avg_time:.4f}s")
        print(f"Throughput: {throughput:.2f} KB/s")
        print(f"File Size: {len(data)/1024:.2f} KB")
        
        return result
    
    def test_vpn(self, trials=5):
        """Test VPN performance"""
        print("\n" + "="*60)
        print("VPN TUNNEL TEST (Encrypted)")
        print("="*60)
        
        data = self.read_file()
        times = []
        
        for i in range(trials):
            tunnel = VPNTunnel()
            server_thread = threading.Thread(target=tunnel.start_server, daemon=True)
            server_thread.start()
            time.sleep(0.1)
            
            start = time.time()
            response = tunnel.send_data(data)
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"Trial {i+1}: {elapsed:.4f}s")
            
            tunnel.running = False
            server_thread.join(timeout=1)
        
        avg_time = sum(times) / len(times) if times else 0.001
        throughput = (len(data) / avg_time) / 1024 if avg_time > 0 else 0
        
        result = {
            'type': 'vpn_encrypted',
            'avg_time': avg_time,
            'throughput_kbps': throughput,
            'file_size_kb': len(data) / 1024
        }
        self.results.append(result)
        
        print(f"\nVPN Average: {avg_time:.4f}s")
        print(f"Throughput: {throughput:.2f} KB/s")
        
        return result
    
    def compare_results(self):
        """Compare baseline vs VPN"""
        if len(self.results) < 2:
            return
        
        baseline = self.results[0]
        vpn = self.results[1]
        
        print("\n" + "="*60)
        print("PERFORMANCE COMPARISON")
        print("="*60)
        print(f"Baseline Time:     {baseline['avg_time']:.4f}s")
        print(f"VPN Time:          {vpn['avg_time']:.4f}s")
        print(f"Slowdown Factor:   {vpn['avg_time']/baseline['avg_time']:.2f}x")
        print(f"\nBaseline Throughput: {baseline['throughput_kbps']:.2f} KB/s")
        print(f"VPN Throughput:      {vpn['throughput_kbps']:.2f} KB/s")
        
        return {
            'baseline': baseline,
            'vpn': vpn,
            'slowdown_factor': vpn['avg_time'] / baseline['avg_time']
        }
    
    def export_results(self, filename='vpn_performance_results.json'):
        """Export results"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults exported to {filename}")


def main():
    """Run VPN system"""
    print("\n" + "="*60)
    print("REAL VPN SYSTEM - PERFORMANCE MEASUREMENT")
    print("="*60)
    
    file_path = 'AliceInWonderland.txt'
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return
    
    tester = VPNPerformanceTester(file_path)
    tester.test_baseline(trials=3)
    tester.test_vpn(trials=3)
    tester.compare_results()
    tester.export_results()
    
    print("\n" + "="*60)
    print("VPN SYSTEM TEST COMPLETE")
    print("="*60)


if __name__ == '__main__':
    main()
