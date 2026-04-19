#!/usr/bin/env python3
"""Windows VPN Screencast Runner - Fixed"""

import subprocess
import time
import webbrowser
import sys
import os

print("VPN Screencast Demo - Windows Fixed")

def ensure_file():
    if not os.path.exists('vpn_tools/AliceInWonderland.txt'):
        print('[+] Creating test file...')
        with open('vpn_tools/AliceInWonderland.txt', 'w') as f:
            f.write('A' * 170*1024)  # 170KB
    print('[+] Test file ready')

ensure_file()

print('\n1. Run perf measure:')
subprocess.run([sys.executable, 'vpn_tools/vpn_perf_windows_fixed.py'])

print('\n2. Show JSON:')
with open('vpn_tools/perf_results_windows.json') as f:
    print(f.read())

print('\n3. Start dashboard:')
dash = subprocess.Popen([sys.executable, 'vpn_tools/dashboard.py'])

time.sleep(3)
print('\n4. Open dashboard & HTML:')
webbrowser.open('http://localhost:5001')
webbrowser.open('file:///c:/Users/Lenovo/project/website/vpn-live-demo.html')

print('\nRECORD 60s NOW!')
time.sleep(60)

dash.terminate()
print('\nDEMO COMPLETE - JSON saved!')

