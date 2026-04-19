#!/usr/bin/env python3
\"\"\"VPN Screencast Demo Runner
Runs auto_demo + dashboard, opens browsers.\"\"\"

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
            print('[!] Curl failed. Create AliceInWonderland.txt manually (170KB any text)')

def run_demo():
    print('🚀 Starting FULL VPN SCREENCAST DEMO...')
    print('=' * 60)
    
    # Ensure test file
    ensure_alice_file()
    
    # Run auto_demo in background (generates data)
    demo_proc = subprocess.Popen([sys.executable, 'auto_demo.py', '--run'])
    
    # Wait 10s for demo to run (tunnel+perf)
    time.sleep(10)
    
    # Start dashboard
    dash_proc = subprocess.Popen([sys.executable, 'dashboard.py'])
    
    # Wait 3s for dashboard startup
    time.sleep(3)
    
    print('\\n🌐 Opening Browsers...')
    
    # Open dashboard
    webbrowser.open('http://localhost:5001')
    
    # Open HTML demo
    webbrowser.open('../website/vpn-live-demo.html')
    webbrowser.open('../website/index.html')
    
    print('\\n⏳ DEMO RUNNING 120s...')
    print('• Watch terminal for auto_demo output')
    print('• Dashboard: localhost:5001 (live charts/logs)')
    print('• HTML Demo: Interactive animations')
    print('\\n📹 Start recording now (Win+G → Record)!')
    
    # Wait full demo time
    time.sleep(120)
    
    # Cleanup
    print('\\n🛑 Stopping...')
    demo_proc.terminate()
    dash_proc.terminate()
    
    print('✅ SCREENCAST READY! Check vpn_tools/*.json files')

if __name__ == '__main__':
    run_demo()
