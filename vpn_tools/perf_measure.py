#!/usr/bin/env python3
"""VPN Performance Measurement
File transfer time, throughput, baseline vs VPN, JSON/CSV output.
Uses AliceInWonderland.txt"""

import subprocess
import time
import json
import csv
import os
from datetime import datetime
from statistics import mean, stdev

ALICE_FILE = 'AliceInWonderland.txt'
SERVER_IP = '10.0.0.2'  # VPN peer IP
HTTP_PORT = 8000

class PerfMeasure:
    def __init__(self):
        self.results = []
    
    def start_server(self, ip='0.0.0.0'):
        """Start simple HTTP server on current dir."""
        print('[*] Starting HTTP server...')
        # Background server (non-blocking)
        subprocess.Popen(['python3', '-m', 'http.server', str(HTTP_PORT)], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        print('[+] Server ready on port 8000')
    
    def wget_transfer(self, url, trials=5):
        """Measure wget transfer time."""
        times = []
        
        for i in range(trials):
            start = time.perf_counter()
            try:
                result = subprocess.run([
                    'wget', '-q', '-O', '/tmp/test.txt', url
                ], capture_output=True, timeout=30, check=True)
                end = time.perf_counter()
                
                transfer_time = end - start
                times.append(transfer_time)
                print(f'Trial {i+1}: {transfer_time:.3f}s')
                
            except subprocess.TimeoutExpired:
                print(f'Trial {i+1}: TIMEOUT')
            except:
                print(f'Trial {i+1}: FAILED')
        
        return times
    
    def measure_baseline(self, trials=5):
        """Local baseline (no VPN)."""
        print('\n=== BASELINE MEASUREMENT ===')
        self.start_server()
        times = self.wget_transfer(f'http://127.0.0.1:{HTTP_PORT}/{ALICE_FILE}', trials)
        
        if times:
            avg_time = mean(times)
            throughput = 170 / avg_time  # KB/s approx
            result = {
                'type': 'baseline',
                'timestamp': datetime.now().isoformat(),
                'trials': trials,
                'avg_time_s': avg_time,
                'throughput_kbs': throughput,
                'times': times
            }
            self.results.append(result)
            print(f'[+] Baseline: {avg_time:.3f}s, {throughput:.1f} KB/s')
            return result
        return None
    
    def measure_vpn(self, server_ip=SERVER_IP, trials=5):
        """VPN tunnel measurement."""
        print('\n=== VPN MEASUREMENT ===')
        url = f'http://{server_ip}:{HTTP_PORT}/{ALICE_FILE}'
        times = self.wget_transfer(url, trials)
        
        if times:
            avg_time = mean(times)
            throughput = 170 / avg_time
            result = {
                'type': 'vpn',
                'server_ip': server_ip,
                'timestamp': datetime.now().isoformat(),
                'trials': trials,
                'avg_time_s': avg_time,
                'throughput_kbs': throughput,
                'times': times
            }
            self.results.append(result)
            print(f'[+] VPN: {avg_time:.3f}s, {throughput:.1f} KB/s')
            return result
        return None
    
    def save_csv(self, filename='perf_results.csv'):
        """Save to CSV."""
        if not self.results:
            print('No results to save')
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)
        print(f'[+] Saved CSV: {filename}')
    
    def save_json(self, filename='perf_results.json'):
        """Save to JSON."""
        if self.results:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f'[+] Saved JSON: {filename}')
    
    def compare(self):
        """Compare baseline vs VPN."""
        baseline = next((r for r in self.results if r['type'] == 'baseline'), None)
        vpn = next((r for r in self.results if r['type'] == 'vpn'), None)
        
        if baseline and vpn:
            overhead = (vpn['avg_time_s'] / baseline['avg_time_s'] - 1) * 100
            print('\n=== COMPARISON ===')
            print(f'Baseline: {baseline["avg_time_s"]:.3f}s ({baseline["throughput_kbs"]:.1f} KB/s)')
            print(f'VPN:      {vpn["avg_time_s"]:.3f}s ({vpn["throughput_kbs"]:.1f} KB/s)')
            print(f'Overhead: +{overhead:.1f}%')

if __name__ == '__main__':
    perf = PerfMeasure()
    
    # Full measurement sequence
    perf.measure_baseline()
    time.sleep(2)  # Let server stabilize
    perf.measure_vpn()
    
    perf.compare()
    perf.save_csv()
    perf.save_json()

