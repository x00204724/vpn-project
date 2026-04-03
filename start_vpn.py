#!/usr/bin/env python3
"""
Simple VPN Systems - Quick Start
No external dependencies required
"""

import subprocess
import sys
import time

def main():
    print("\n" + "="*70)
    print("🔒 SIMPLE VPN SYSTEMS - QUICK START")
    print("="*70)
    print("\nNo external dependencies required!")
    print("\nAvailable systems:")
    print("  1. VPN Server (Encrypted multi-client)")
    print("  2. VPN Dashboard (Web monitoring)")
    print("  3. Run Both")
    print("  4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        print("\n[*] Starting VPN Server...")
        print("[*] Usage: python3 simple_vpn_server.py client localhost user1 password123")
        subprocess.run([sys.executable, 'simple_vpn_server.py', 'server'])
    
    elif choice == '2':
        print("\n[*] Starting VPN Dashboard...")
        print("[*] Open browser: http://localhost:8000")
        subprocess.run([sys.executable, 'simple_vpn_dashboard.py'])
    
    elif choice == '3':
        print("\n[*] Starting both systems...")
        print("[*] VPN Server on port 8443")
        print("[*] Dashboard on http://localhost:8000")
        
        # Start server in background
        server_proc = subprocess.Popen([sys.executable, 'simple_vpn_server.py', 'server'])
        time.sleep(2)
        
        # Start dashboard
        try:
            subprocess.run([sys.executable, 'simple_vpn_dashboard.py'])
        except KeyboardInterrupt:
            server_proc.terminate()
    
    elif choice == '4':
        print("\n[*] Goodbye!")
    
    else:
        print("[-] Invalid choice")


if __name__ == '__main__':
    main()
