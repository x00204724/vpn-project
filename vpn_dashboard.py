#!/usr/bin/env python3
"""
VPN Management Dashboard - Complete Working System
Real-time monitoring, statistics, and control interface
"""

import json
import time
import threading
from datetime import datetime
from flask import Flask, render_template_string, jsonify, request
import psutil
import socket

app = Flask(__name__)

class VPNDashboard:
    def __init__(self):
        self.vpn_servers = {}
        self.vpn_clients = {}
        self.performance_data = []
        self.alerts = []
        self.start_time = datetime.now()
        
    def add_vpn_server(self, name, host, port, protocol='TLS'):
        """Add VPN server to dashboard"""
        self.vpn_servers[name] = {
            'name': name,
            'host': host,
            'port': port,
            'protocol': protocol,
            'status': 'offline',
            'connections': 0,
            'bytes_sent': 0,
            'bytes_received': 0,
            'uptime': 0,
            'cpu_usage': 0,
            'memory_usage': 0,
            'last_check': None
        }
    
    def add_vpn_client(self, name, server, username, status='disconnected'):
        """Add VPN client to dashboard"""
        self.vpn_clients[name] = {
            'name': name,
            'server': server,
            'username': username,
            'status': status,
            'vpn_ip': None,
            'connected_at': None,
            'bytes_sent': 0,
            'bytes_received': 0,
            'latency': 0
        }
    
    def check_server_status(self, server_name):
        """Check VPN server status"""
        server = self.vpn_servers.get(server_name)
        if not server:
            return False
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((server['host'], server['port']))
            sock.close()
            
            if result == 0:
                server['status'] = 'online'
                server['last_check'] = datetime.now().isoformat()
                return True
            else:
                server['status'] = 'offline'
                self.add_alert(f"Server {server_name} is offline")
                return False
        
        except Exception as e:
            server['status'] = 'error'
            self.add_alert(f"Error checking {server_name}: {str(e)}")
            return False
    
    def update_server_stats(self, server_name, connections=0, bytes_sent=0, bytes_received=0):
        """Update server statistics"""
        server = self.vpn_servers.get(server_name)
        if server:
            server['connections'] = connections
            server['bytes_sent'] += bytes_sent
            server['bytes_received'] += bytes_received
            server['uptime'] = (datetime.now() - self.start_time).total_seconds()
    
    def update_client_stats(self, client_name, latency=0, bytes_sent=0, bytes_received=0):
        """Update client statistics"""
        client = self.vpn_clients.get(client_name)
        if client:
            client['latency'] = latency
            client['bytes_sent'] += bytes_sent
            client['bytes_received'] += bytes_received
    
    def add_alert(self, message):
        """Add alert to dashboard"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'severity': 'warning'
        }
        self.alerts.append(alert)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    def get_dashboard_data(self):
        """Get complete dashboard data"""
        return {
            'timestamp': datetime.now().isoformat(),
            'uptime': (datetime.now() - self.start_time).total_seconds(),
            'servers': self.vpn_servers,
            'clients': self.vpn_clients,
            'alerts': self.alerts[-10:],  # Last 10 alerts
            'summary': {
                'total_servers': len(self.vpn_servers),
                'online_servers': sum(1 for s in self.vpn_servers.values() if s['status'] == 'online'),
                'total_clients': len(self.vpn_clients),
                'connected_clients': sum(1 for c in self.vpn_clients.values() if c['status'] == 'connected'),
                'total_bytes_sent': sum(s['bytes_sent'] for s in self.vpn_servers.values()),
                'total_bytes_received': sum(s['bytes_received'] for s in self.vpn_servers.values())
            }
        }


# Initialize dashboard
dashboard = VPNDashboard()

# Add sample servers
dashboard.add_vpn_server('PriTunnel-1', '192.168.1.33', 443, 'TLS 1.3')
dashboard.add_vpn_server('Azure-VPN', '40.71.0.1', 443, 'IPSec')
dashboard.add_vpn_server('WireGuard-1', '203.0.113.1', 51820, 'WireGuard')

# Add sample clients
dashboard.add_vpn_client('user1', 'PriTunnel-1', 'user1@example.com', 'connected')
dashboard.add_vpn_client('user2', 'Azure-VPN', 'user2@example.com', 'connected')
dashboard.add_vpn_client('user3', 'WireGuard-1', 'user3@example.com', 'disconnected')

# HTML Dashboard Template
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>VPN Management Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #1a1a1a; color: #fff; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { background: #2a2a2a; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .header h1 { font-size: 28px; margin-bottom: 10px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .stat-card { background: #2a2a2a; padding: 15px; border-radius: 5px; border-left: 4px solid #00ff00; }
        .stat-card h3 { font-size: 12px; color: #888; margin-bottom: 5px; }
        .stat-card .value { font-size: 24px; font-weight: bold; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px; }
        .card { background: #2a2a2a; padding: 20px; border-radius: 5px; }
        .card h2 { font-size: 18px; margin-bottom: 15px; border-bottom: 2px solid #00ff00; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #444; }
        th { background: #1a1a1a; font-weight: bold; }
        .status-online { color: #00ff00; }
        .status-offline { color: #ff0000; }
        .status-connected { color: #00ff00; }
        .status-disconnected { color: #ff8800; }
        .alert { background: #3a2a2a; padding: 10px; margin: 5px 0; border-left: 3px solid #ff8800; border-radius: 3px; }
        .refresh-btn { background: #00ff00; color: #000; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; font-weight: bold; }
        .refresh-btn:hover { background: #00cc00; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 VPN Management Dashboard</h1>
            <p>Real-time monitoring and control</p>
            <button class="refresh-btn" onclick="location.reload()">Refresh</button>
        </div>
        
        <div class="summary" id="summary"></div>
        
        <div class="grid">
            <div class="card">
                <h2>VPN Servers</h2>
                <table id="servers-table">
                    <thead>
                        <tr>
                            <th>Server</th>
                            <th>Status</th>
                            <th>Connections</th>
                            <th>Data Sent</th>
                            <th>Data Received</th>
                        </tr>
                    </thead>
                    <tbody id="servers-body"></tbody>
                </table>
            </div>
            
            <div class="card">
                <h2>VPN Clients</h2>
                <table id="clients-table">
                    <thead>
                        <tr>
                            <th>Client</th>
                            <th>Server</th>
                            <th>Status</th>
                            <th>Latency</th>
                            <th>VPN IP</th>
                        </tr>
                    </thead>
                    <tbody id="clients-body"></tbody>
                </table>
            </div>
        </div>
        
        <div class="card" style="margin-top: 20px;">
            <h2>Recent Alerts</h2>
            <div id="alerts"></div>
        </div>
    </div>
    
    <script>
        function updateDashboard() {
            fetch('/api/dashboard')
                .then(response => response.json())
                .then(data => {
                    // Update summary
                    const summary = data.summary;
                    document.getElementById('summary').innerHTML = `
                        <div class="stat-card">
                            <h3>Online Servers</h3>
                            <div class="value">${summary.online_servers}/${summary.total_servers}</div>
                        </div>
                        <div class="stat-card">
                            <h3>Connected Clients</h3>
                            <div class="value">${summary.connected_clients}/${summary.total_clients}</div>
                        </div>
                        <div class="stat-card">
                            <h3>Data Sent</h3>
                            <div class="value">${(summary.total_bytes_sent / 1024 / 1024).toFixed(2)} MB</div>
                        </div>
                        <div class="stat-card">
                            <h3>Data Received</h3>
                            <div class="value">${(summary.total_bytes_received / 1024 / 1024).toFixed(2)} MB</div>
                        </div>
                    `;
                    
                    // Update servers table
                    let serversHtml = '';
                    for (const [name, server] of Object.entries(data.servers)) {
                        const statusClass = server.status === 'online' ? 'status-online' : 'status-offline';
                        serversHtml += `
                            <tr>
                                <td>${server.name}</td>
                                <td class="${statusClass}">${server.status.toUpperCase()}</td>
                                <td>${server.connections}</td>
                                <td>${(server.bytes_sent / 1024 / 1024).toFixed(2)} MB</td>
                                <td>${(server.bytes_received / 1024 / 1024).toFixed(2)} MB</td>
                            </tr>
                        `;
                    }
                    document.getElementById('servers-body').innerHTML = serversHtml;
                    
                    // Update clients table
                    let clientsHtml = '';
                    for (const [name, client] of Object.entries(data.clients)) {
                        const statusClass = client.status === 'connected' ? 'status-connected' : 'status-disconnected';
                        clientsHtml += `
                            <tr>
                                <td>${client.name}</td>
                                <td>${client.server}</td>
                                <td class="${statusClass}">${client.status.toUpperCase()}</td>
                                <td>${client.latency.toFixed(2)} ms</td>
                                <td>${client.vpn_ip || 'N/A'}</td>
                            </tr>
                        `;
                    }
                    document.getElementById('clients-body').innerHTML = clientsHtml;
                    
                    // Update alerts
                    let alertsHtml = '';
                    for (const alert of data.alerts) {
                        alertsHtml += `<div class="alert">${alert.message}</div>`;
                    }
                    document.getElementById('alerts').innerHTML = alertsHtml || '<p>No alerts</p>';
                });
        }
        
        // Update dashboard every 5 seconds
        updateDashboard();
        setInterval(updateDashboard, 5000);
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard_page():
    """Serve dashboard page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/dashboard')
def api_dashboard():
    """API endpoint for dashboard data"""
    return jsonify(dashboard.get_dashboard_data())

@app.route('/api/servers')
def api_servers():
    """API endpoint for servers"""
    return jsonify(dashboard.vpn_servers)

@app.route('/api/clients')
def api_clients():
    """API endpoint for clients"""
    return jsonify(dashboard.vpn_clients)

@app.route('/api/alerts')
def api_alerts():
    """API endpoint for alerts"""
    return jsonify(dashboard.alerts)

@app.route('/api/server/<name>/status')
def api_server_status(name):
    """Check specific server status"""
    dashboard.check_server_status(name)
    server = dashboard.vpn_servers.get(name)
    return jsonify(server) if server else jsonify({'error': 'Server not found'}), 404

@app.route('/api/server/<name>/stats', methods=['POST'])
def api_update_stats(name):
    """Update server statistics"""
    data = request.json
    dashboard.update_server_stats(
        name,
        connections=data.get('connections', 0),
        bytes_sent=data.get('bytes_sent', 0),
        bytes_received=data.get('bytes_received', 0)
    )
    return jsonify({'status': 'updated'})

def monitor_servers():
    """Background thread to monitor servers"""
    while True:
        for server_name in dashboard.vpn_servers:
            dashboard.check_server_status(server_name)
        time.sleep(30)

def main():
    """Main function"""
    print("\n" + "="*60)
    print("VPN MANAGEMENT DASHBOARD")
    print("="*60)
    print("\n[*] Starting VPN Dashboard...")
    print("[*] Dashboard URL: http://localhost:5000")
    print("[*] API Endpoints:")
    print("    - GET /api/dashboard - Complete dashboard data")
    print("    - GET /api/servers - All servers")
    print("    - GET /api/clients - All clients")
    print("    - GET /api/alerts - All alerts")
    print("    - GET /api/server/<name>/status - Check server status")
    print("    - POST /api/server/<name>/stats - Update server stats")
    
    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_servers)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
