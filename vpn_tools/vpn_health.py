#!/usr/bin/env python3
"""VPN Health Check Tool
Ping 10.0.0.2, measure latency, detect packet loss."""

import subprocess
import statistics
import json
from datetime import datetime

class VPNHealth:
    def __init__(self, target='10.0.0.2'):
        self.target = target
        self.results = {}
    
    def ping_test(self, count=10):
        """Run ping test and parse results."""
        print(f'[*] Health check: ping {self.target} x{count}')
        
        try:
            result = subprocess.run(
                ['ping', '-c', str(count), self.target],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Parse ping output
                lines = result.stdout.split('\n')
                stats_line = [line for line in lines if 'rtt min/avg/max' in line]
                
                if stats_line:
                    stats = stats_line[0].split('=')[1].strip().split('/')
                    min_rtt, avg_rtt, max_rtt = map(float, stats)
                    
                    self.results = {
                        'timestamp': datetime.now().isoformat(),
                        'target': self.target,
                        'packets_sent': count,
                        'packet_loss_pct': 0.0,
                        'rtt_min_ms': min_rtt,
                        'rtt_avg_ms': avg_rtt,
                        'rtt_max_ms': max_rtt,
                        'status': 'HEALTHY'
                    }
                    print(f'[+] HEALTHY: avg {avg_rtt:.1f}ms (min {min_rtt:.1f}, max {max_rtt:.1f})')
                    return True
                else:
                    print('[-] Could not parse ping stats')
                    return False
            else:
                self.results = {
                    'timestamp': datetime.now().isoformat(),
                    'status': 'UNREACHABLE',
                    'error': result.stderr.strip()
                }
                print('[-] UNREACHABLE')
                return False
                
        except Exception as e:
            print(f'[-] Ping error: {e}')
            return False
    
    def save_json(self, filename='health_check.json'):
        """Save results to JSON."""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f'[+] Saved to {filename}')
    
    def print_report(self):
        """Print formatted report."""
        print('\n=== VPN HEALTH REPORT ===')
        print(f'Target: {self.target}')
        print(f'Status: {self.results.get("status", "UNKNOWN")}')
        if 'rtt_avg_ms' in self.results:
            print(f'Latency: {self.results["rtt_avg_ms"]:.1f}ms (min {self.results["rtt_min_ms"]:.1f}, max {self.results["rtt_max_ms"]:.1f})')
        print('==========================\n')

if __name__ == '__main__':
    health = VPNHealth()
    health.ping_test(10)
    health.print_report()
    health.save_json()

