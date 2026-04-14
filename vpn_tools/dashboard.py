#!/usr/bin/env python3
\"\"\"Simple Flask Dashboard - VPN Status & Results
Run: python dashboard.py
Open: http://localhost:5001\"\"\"
from flask import Flask, jsonify, render_template_string
import os
import json
from datetime import datetime

app = Flask(__name__)

# Load data
def load_data():
    data = {}
    
    # Health check
    try:
        with open('vpn_tools/health_check.json', 'r') as f:
            data['health'] = json.load(f)
    except:
        data['health'] = {'status': 'No data'}
    
    # Perf
    try:
        with open('vpn_tools/perf_results.json', 'r') as f:
            data['perf'] = json.load(f)
    except:
        data['perf'] = []
    
    # Logs
    try:
        with open('vpn_tools/demo_log.json', 'r') as f:
            data['logs'] = json.load(f)[-10:]  # Last 10
    except:
        data['logs'] = []
    
    data['time'] = datetime.now().strftime('%H:%M:%S')
    return data

@app.route('/')
def index():
    data = load_data()
    html = '''
<!doctype html>
<html>
<head><title>VPN Dashboard</title>
<style>
body { font-family: Arial; margin: 40px; background: #f5f5f5; }
.card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
h2 { color: #333; }
.status { font-size: 24px; font-weight: bold; }
.healthy { color: green; }
.unhealthy { color: red; }
.logs { background: #1e1e1e; color: #0f0; padding: 15px; border-radius: 4px; max-height: 300px; overflow-y: auto; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
th { background: #667eea; color: white; }
</style></head>
<body>
    <h1>VPN Status Dashboard</h1>
    <div class="card">
        <h2>Health Status</h2>
        <div class="status {{ 'healthy' if data.health.status == "HEALTHY" else 'unhealthy' }}">{{ data.health.status }}</div>
        {% if data.health.packet_loss_pct > 0 %}<p>Packet Loss: {{ data.health.packet_loss_pct }}%</p>{% endif %}
    </div>
    
    <div class="card">
        <h2>Latest Performance</h2>
        {% if data.perf %}
        <table>
            <tr><th>Test Type</th><th>Time (s)</th><th>Throughput (KB/s)</th></tr>
            {% for test in data.perf[-2:] %}
            <tr><td>{{ test.type.upper() }}</td><td>{{ "%.3f"|format(test.avg_time_s) }}</td><td>{{ "%.1f"|format(test.throughput_kbs) }}</td></tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No performance data</p>
        {% endif %}
    </div>
    
    <div class="card">
        <h2>Recent Logs</h2>
        <div class="logs">
            {% for log in data.logs %}
            <div>[{{ log.timestamp }}] {{ log.level }}: {{ log.message }}</div>
            {% endfor %}
        </div>
    </div>
    
    <div style="margin-top: 30px; font-size: 12px; color: #666;">
        Last updated: {{ data.time }} | <a href="/api/status">API</a> | <a href="/api/logs">Logs</a>
    </div>
</body>
</html>
    '''
    return render_template_string(html, data=data)
    
@app.route('/api/status')
def api_status():
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    print('VPN Dashboard running on http://localhost:5001')
    print('Ctrl+C to stop')
    app.run(host='0.0.0.0', port=5001, debug=False)

