#!/usr/bin/env python3
"""
VPN Screencast Demo Runner - Fixed for WSL
Runs auto_demo + dashboard, opens browsers.
"""

import subprocess
import time
import webbrowser
import sys
import os

def ensure_alice_file():
    alice_path = 'AliceInWonderland.txt'
    if not os.path.exists(alice_path):
        print('[!] Downloading AliceInWonderland.txt (170KB test file)')
        try:
            subprocess.run(['curl', '-o', alice_path, 'https://www.gutenberg.org/files/11/11-0.txt'], check=True)
            print('[+] Downloaded')
        except:
            print('[!] Curl failed. Alice.txt already exists')
    
def run_demo():
    print('🚀 Starting FULL VPN SCREENCAST DEMO...')
    print('=' * 60)
    
    # Ensure test file
    ensure_alice_file()
    
    print('[INFO] Running auto_demo.py (WireGuard + perf)...')
    # Run auto_demo
    result = subprocess.run([sys.executable, 'auto_demo.py', '--run'], capture_output=False)
    print('[INFO] auto_demo complete!')
    
    print('[INFO] Starting dashboard (localhost:5001)...')
    # Start dashboard (non-blocking)
    dash_proc = subprocess.Popen([sys.executable, 'dashboard.py'])
    time.sleep(3)
    
    print('\\n🌐 Opening Browsers...')
    webbrowser.open('http://localhost:5001')
    webbrowser.open('../website/vpn-live-demo.html')
    webbrowser.open('../website/index.html')
    
    print('\\n⏳ DEMO RUNNING 60s (dashboard + HTML)...')
    print('• Terminal: auto_demo output above')
    print('• Dashboard: localhost:5001 (charts/logs)')
    print('• HTML Demos: Interactive + charts')
    print('\\n📹 RECORD NOW (Win+G)!')
    
    time.sleep(60)
    
    print('\\n🛑 Stopping dashboard...')
    dash_proc.terminate()
    
    print('✅ SCREENCAST COMPLETE!')
    print('Files: vpn_measurements.json, demo_log.json, health_check.json')

if __name__ == '__main__':
    run_demo()
