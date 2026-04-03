#!/usr/bin/env python3
"""
Simple VPN Dashboard - No External Dependencies
Uses built-in Python HTTP server
"""

import http.server
import socketserver
import json
import threading
import time
from datetime import datetime

class VPNDashboardHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for VPN dashboard"""
    
    dashboard_data = {
        'servers': {
            'VPN-Server-1': {
                'name': 'VPN-Server-1',
                'host': 'localhost',
                'port': 8443,
                'status': 'online',
                'connections': 0,
                'bytes_sent': 0,
                'bytes_received': 0
            },
            'Azure-VPN': {
                'name': 'Azure-VPN',
                'host': '40.71.0.1',
                'port': 443,
                'status': 'online',
                'connections': 0,
                'bytes_sent': 0,
                'bytes_received': 0
            }
        },
        'clients': {
            'user1': {
                'name': 'user1',
                'server': 'VPN-Server-1',
                'status': 'disconnected',
                'vpn_ip': None,
                'latency': 0
            },
            'user2': {
                'name': 'user2',
                'server': 'Azure-VPN',
                'status': 'disconnected',
                'vpn_ip': None,
                'latency': 0
            }
        },
        'stats': {
            'total_connections': 0,
            'total_bytes': 0,
            'uptime': 0
        }
    }
    
    HTML_TEMPLATE = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>VPN Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .header {
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
                color: white;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            .header h1 { font-size: 32px; margin-bottom: 10px; }
            .header p { font-size: 14px; opacity: 0.9; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .card {
                background: rgba(255,255,255,0.95);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            .card h2 { font-size: 18px; margin-bottom: 15px; color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
            .stat { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
            .stat-label { color: #666; }
            .stat-value { font-weight: bold; color: #333; }
            .status-online { color: #4caf50; font-weight: bold; }
            .status-offline { color: #f44336; font-weight: bold; }
            .status-connected { color: #4caf50; }
            .status-disconnected { color: #ff9800; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #667eea; color: white; }
            tr:hover { background: #f5f5f5; }
            .refresh-btn {
                background: #667eea;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                margin-top: 10px;
            }
            .refresh-btn:hover { background: #764ba2; }
            .alert { background: #fff3cd; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #ffc107; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔒 VPN Management Dashboard</h1>
                <p>Real-time VPN monitoring and control</p>
            </div>
            
            <div class="alert">
                <strong>✅ System Status:</strong> All VPN systems operational
            </div>
            
            <div class="grid">
                <div class="card">
                    <h2>📊 Statistics</h2>
                    <div class="stat">
                        <span class="stat-label">Total Connections:</span>
                        <span class="stat-value" id="total-connections">0</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Total Data:</span>
                        <span class="stat-value" id="total-data">0 MB</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Uptime:</span>
                        <span class="stat-value" id="uptime">0s</span>
                    </div>
                </div>
                
                <div class="card">
                    <h2>🖥️ VPN Servers</h2>
                    <div class="stat">
                        <span class="stat-label">VPN-Server-1:</span>
                        <span class="status-online">● Online</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Azure-VPN:</span>
                        <span class="status-online">● Online</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">Hybrid-VPN:</span>
                        <span class="status-online">● Online</span>
                    </div>
                </div>
                
                <div class="card">
                    <h2>👥 Connected Clients</h2>
                    <div class="stat">
                        <span class="stat-label">user1:</span>
                        <span class="status-disconnected">Disconnected</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">user2:</span>
                        <span class="status-disconnected">Disconnected</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">admin:</span>
                        <span class="status-disconnected">Disconnected</span>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>📈 VPN Servers Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Server</th>
                            <th>Host</th>
                            <th>Port</th>
                            <th>Status</th>
                            <th>Connections</th>
                        </tr>
                    </thead>
                    <tbody id="servers-table">
                        <tr>
                            <td>VPN-Server-1</td>
                            <td>localhost</td>
                            <td>8443</td>
                            <td><span class="status-online">Online</span></td>
                            <td>0</td>
                        </tr>
                        <tr>
                            <td>Azure-VPN</td>
                            <td>40.71.0.1</td>
                            <td>443</td>
                            <td><span class="status-online">Online</span></td>
                            <td>0</td>
                        </tr>
                        <tr>
                            <td>Hybrid-VPN</td>
                            <td>192.168.1.1</td>
                            <td>443</td>
                            <td><span class="status-online">Online</span></td>
                            <td>0</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="card" style="margin-top: 20px;">
                <h2>🔧 Quick Commands</h2>
                <pre style="background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto;">
# Start VPN Server
python3 simple_vpn_server.py server

# Connect VPN Client
python3 simple_vpn_server.py client localhost user1 password123

# View Dashboard
Open: http://localhost:8000

# Test VPN Connection
ping 10.8.0.2
                </pre>
                <button class="refresh-btn" onclick="location.reload()">Refresh Dashboard</button>
            </div>
        </div>
        
        <script>
            // Update dashboard every 5 seconds
            function updateDashboard() {
                fetch('/api/dashboard')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('total-connections').textContent = data.stats.total_connections;
                        document.getElementById('total-data').textContent = (data.stats.total_bytes / 1024 / 1024).toFixed(2) + ' MB';
                        document.getElementById('uptime').textContent = Math.floor(data.stats.uptime) + 's';
                    })
                    .catch(err => console.log('Dashboard update failed'));
            }
            
            updateDashboard();
            setInterval(updateDashboard, 5000);
        </script>
    </body>
    </html>
    '''
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.HTML_TEMPLATE.encode())
        
        elif self.path == '/api/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.dashboard_data).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def start_dashboard(port=8000):
    """Start VPN dashboard server"""
    handler = VPNDashboardHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\n{'='*60}")
        print(f"[+] VPN Dashboard started")
        print(f"[+] Open browser: http://localhost:{port}")
        print(f"[+] Press Ctrl+C to stop")
        print(f"{'='*60}\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Dashboard stopped")


if __name__ == '__main__':
    start_dashboard(port=8000)
