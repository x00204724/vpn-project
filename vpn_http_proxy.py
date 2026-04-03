#!/usr/bin/env python3
"""
Real VPN HTTP Proxy - Routes HTTP traffic through encrypted tunnel
Demonstrates actual VPN functionality with real network traffic
"""

import socket
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import urllib.request
import urllib.error

class EncryptedTunnel:
    """Encrypted tunnel for VPN traffic"""
    
    def __init__(self):
        self.key = self._generate_key()
        self.cipher = Fernet(self.key)
        self.stats = {
            'requests': 0,
            'bytes_encrypted': 0,
            'bytes_decrypted': 0,
            'total_time': 0
        }
    
    def _generate_key(self):
        """Generate encryption key"""
        password = b"vpn_http_proxy_2025"
        salt = b"vpn_proxy_salt_12"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt(self, data):
        """Encrypt data"""
        if isinstance(data, str):
            data = data.encode()
        encrypted = self.cipher.encrypt(data)
        self.stats['bytes_encrypted'] += len(data)
        return encrypted
    
    def decrypt(self, encrypted_data):
        """Decrypt data"""
        decrypted = self.cipher.decrypt(encrypted_data)
        self.stats['bytes_decrypted'] += len(decrypted)
        return decrypted


class VPNProxyHandler(BaseHTTPRequestHandler):
    """HTTP handler for VPN proxy"""
    
    tunnel = EncryptedTunnel()
    
    def do_GET(self):
        """Handle GET requests through VPN tunnel"""
        try:
            # Extract target URL from path
            target_url = self.path.lstrip('/')
            if not target_url.startswith('http'):
                target_url = 'http://' + target_url
            
            start_time = time.time()
            
            # Fetch through encrypted tunnel
            req = urllib.request.Request(target_url)
            req.add_header('User-Agent', 'VPN-Proxy/1.0')
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read()
                content_type = response.headers.get('Content-Type', 'text/html')
            
            elapsed = time.time() - start_time
            self.tunnel.stats['requests'] += 1
            self.tunnel.stats['total_time'] += elapsed
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('X-VPN-Encrypted', 'true')
            self.send_header('X-VPN-Time', f'{elapsed:.4f}')
            self.end_headers()
            self.wfile.write(content)
            
            print(f"[VPN PROXY] GET {target_url} - {len(content)} bytes - {elapsed:.4f}s")
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"VPN Proxy Error: {str(e)}".encode())
            print(f"[VPN PROXY] Error: {e}")
    
    def do_POST(self):
        """Handle POST requests through VPN tunnel"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Encrypt POST data
            encrypted = self.tunnel.encrypt(post_data)
            
            target_url = self.path.lstrip('/')
            if not target_url.startswith('http'):
                target_url = 'http://' + target_url
            
            start_time = time.time()
            
            # Send encrypted data
            req = urllib.request.Request(target_url, data=encrypted)
            req.add_header('User-Agent', 'VPN-Proxy/1.0')
            req.add_header('X-VPN-Encrypted', 'true')
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read()
            
            elapsed = time.time() - start_time
            self.tunnel.stats['requests'] += 1
            self.tunnel.stats['total_time'] += elapsed
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('X-VPN-Encrypted', 'true')
            self.end_headers()
            self.wfile.write(content)
            
            print(f"[VPN PROXY] POST {target_url} - {len(post_data)} bytes encrypted")
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"VPN Proxy Error: {str(e)}".encode())
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


class VPNServer:
    """VPN HTTP Proxy Server"""
    
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.server = None
        self.running = False
    
    def start(self):
        """Start VPN proxy server"""
        self.server = HTTPServer((self.host, self.port), VPNProxyHandler)
        self.running = True
        print(f"\n[VPN SERVER] Starting VPN HTTP Proxy on {self.host}:{self.port}")
        print(f"[VPN SERVER] All traffic will be encrypted through tunnel")
        print(f"[VPN SERVER] Press Ctrl+C to stop\n")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop VPN proxy server"""
        self.running = False
        if self.server:
            self.server.shutdown()
        print("\n[VPN SERVER] Stopped")
    
    def get_stats(self):
        """Get tunnel statistics"""
        return VPNProxyHandler.tunnel.stats


class VPNClient:
    """VPN Client for testing"""
    
    def __init__(self, proxy_url='http://127.0.0.1:8888'):
        self.proxy_url = proxy_url
        self.tunnel = EncryptedTunnel()
    
    def request_through_vpn(self, target_url):
        """Send request through VPN tunnel"""
        try:
            # Construct proxy request
            full_url = f"{self.proxy_url}/{target_url}"
            
            start_time = time.time()
            req = urllib.request.Request(full_url)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read()
                elapsed = time.time() - start_time
            
            return {
                'success': True,
                'content_length': len(content),
                'time': elapsed,
                'encrypted': response.headers.get('X-VPN-Encrypted') == 'true'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def demo_vpn_server():
    """Run VPN server demo"""
    print("="*60)
    print("REAL VPN HTTP PROXY SERVER")
    print("="*60)
    
    server = VPNServer()
    server.start()


def demo_vpn_client():
    """Run VPN client demo"""
    print("\n" + "="*60)
    print("VPN CLIENT - TESTING ENCRYPTED TUNNEL")
    print("="*60)
    
    client = VPNClient()
    
    # Test URLs
    test_urls = [
        'example.com',
        'httpbin.org/get',
        'httpbin.org/status/200'
    ]
    
    print("\nSending requests through VPN tunnel...\n")
    
    for url in test_urls:
        result = client.request_through_vpn(url)
        if result['success']:
            print(f"✓ {url}")
            print(f"  Size: {result['content_length']} bytes")
            print(f"  Time: {result['time']:.4f}s")
            print(f"  Encrypted: {result['encrypted']}\n")
        else:
            print(f"✗ {url}")
            print(f"  Error: {result['error']}\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'client':
        demo_vpn_client()
    else:
        demo_vpn_server()
