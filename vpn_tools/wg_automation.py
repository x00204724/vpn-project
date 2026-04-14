#!/usr/bin/env python3
"""WireGuard VPN Automation - WSL Ubuntu
Tunnel up/down, handshake check, connectivity test."""

import subprocess
import time
import sys

class WGAutomation:
    def __init__(self, config='wg0'):
        self.config = config
        self.is_up = False
    
    def up(self):
        """Bring tunnel up (sudo wg-quick up wg0)"""
        try:
            subprocess.run(['sudo', 'wg-quick', 'up', self.config], check=True, capture_output=True)
            print(f'[+] {self.config} UP')
            self.is_up = True
            return True
        except subprocess.CalledProcessError as e:
            print(f'[-] Failed to start {self.config}: {e}')
            return False
    
    def down(self):
        """Bring tunnel down"""
        try:
            subprocess.run(['sudo', 'wg-quick', 'down', self.config], check=True, capture_output=True)
            print(f'[+] {self.config} DOWN')
            self.is_up = False
            return True
        except subprocess.CalledProcessError:
            print(f'[-] Failed to stop {self.config}')
            return False
    
    def handshake_status(self):
        """Check latest handshake time"""
        try:
            result = subprocess.run(['wg', 'show', self.config, 'latest-handshakes'], capture_output=True, text=True, check=True)
            handshakes = result.stdout.strip()
            if handshakes:
                print(f'[+] Handshakes OK: {handshakes}')
                return True
            else:
                print('[-] No handshakes detected')
                return False
        except:
            print('[-] Handshake check failed')
            return False
    
    def ping_test(self, target='10.0.0.2', count=4):
        """Ping target through tunnel"""
        print(f'[*] Pinging {target} ({count}x)...')
        try:
            result = subprocess.run(['ping', '-c', str(count), target], capture_output=True, text=True, timeout=10)
            print(result.stdout)
            if result.returncode == 0:
                print('[+] Ping SUCCESS')
                return True
            else:
                print('[-] Ping FAILED')
                return False
        except:
            print('[-] Ping timeout/error')
            return False
    
    def status(self):
        """Full status report"""
        if not self.is_up:
            print('[!] Tunnel down')
            return False
        
        print(f'\n=== {self.config} Status ===')
        self.handshake_status()
        self.ping_test()
        print('========================\n')
        return True

if __name__ == '__main__':
    wg = WGAutomation()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'up':
            wg.up()
        elif cmd == 'down':
            wg.down()
        elif cmd == 'status':
            wg.status()
        else:
            print('Usage: wg_automation.py [up|down|status]')
    else:
        wg.status()

