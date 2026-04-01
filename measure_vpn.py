#!/usr/bin/env python3
"""
VPN Performance Measurement Script
Measures file transfer latency and throughput across different VPN tunnels
"""

import time
import subprocess
import statistics
import json
from datetime import datetime
from pathlib import Path

# Configuration
REMOTE_HOST = "192.168.2.33"  # Ubuntu VM on remote side (Site B)
LOCAL_HOST = "192.168.1.33"   # Ubuntu VM on local side (Site A)
FILE_URL = f"http://{REMOTE_HOST}:8000/AliceInWonderland.txt"
OUTPUT_FILE = "test_file.txt"
NUM_TRIALS = 20
RESULTS_FILE = "vpn_measurements.json"

class VPNMeasurement:
    def __init__(self, vpn_name, description=""):
        self.vpn_name = vpn_name
        self.description = description
        self.times = []
        self.latencies = []
        self.throughputs = []
        
    def measure_transfer(self, file_size_kb=170):
        """
        Measure single file transfer
        Returns: (transfer_time_seconds, throughput_kb_s)
        """
        try:
            start_time = time.time()
            
            # Use curl to download file and measure time
            result = subprocess.run(
                ['curl', '-s', '-o', OUTPUT_FILE, FILE_URL],
                capture_output=True,
                timeout=30
            )
            
            elapsed = time.time() - start_time
            
            if result.returncode == 0:
                # Calculate throughput
                throughput = file_size_kb / elapsed if elapsed > 0 else 0
                return elapsed, throughput
            else:
                print(f"  ❌ Transfer failed: {result.stderr.decode()}")
                return None, None
                
        except subprocess.TimeoutExpired:
            print(f"  ❌ Transfer timeout (>30s)")
            return None, None
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return None, None
    
    def measure_latency(self):
        """
        Measure RTT latency using ping
        Returns: latency in milliseconds
        """
        try:
            result = subprocess.run(
                ['ping', '-n', '1', REMOTE_HOST],
                capture_output=True,
                timeout=5
            )
            
            output = result.stdout.decode()
            # Parse ping output for time
            if 'time=' in output:
                time_str = output.split('time=')[1].split('ms')[0].strip()
                return float(time_str)
            else:
                return None
                
        except Exception as e:
            print(f"  ❌ Ping failed: {e}")
            return None
    
    def run_trials(self, num_trials=NUM_TRIALS):
        """Run multiple transfer trials"""
        print(f"\n📊 Testing {self.vpn_name}")
        print(f"   Description: {self.description}")
        print(f"   Running {num_trials} trials...")
        
        successful_trials = 0
        
        for trial in range(1, num_trials + 1):
            # Measure latency
            latency = self.measure_latency()
            if latency:
                self.latencies.append(latency)
            
            # Measure transfer
            transfer_time, throughput = self.measure_transfer()
            
            if transfer_time and throughput:
                self.times.append(transfer_time)
                self.throughputs.append(throughput)
                successful_trials += 1
                
                print(f"   Trial {trial:2d}: {transfer_time:.3f}s | {throughput:.0f} KB/s", end="")
                if latency:
                    print(f" | RTT: {latency:.1f}ms")
                else:
                    print()
            else:
                print(f"   Trial {trial:2d}: ❌ FAILED")
            
            # Small delay between trials
            time.sleep(0.5)
        
        print(f"   ✅ Completed: {successful_trials}/{num_trials} successful")
        return successful_trials > 0
    
    def get_statistics(self):
        """Calculate statistics from measurements"""
        if not self.times:
            return None
        
        return {
            'vpn_name': self.vpn_name,
            'description': self.description,
            'trials': len(self.times),
            'transfer_time': {
                'mean': statistics.mean(self.times),
                'median': statistics.median(self.times),
                'stdev': statistics.stdev(self.times) if len(self.times) > 1 else 0,
                'min': min(self.times),
                'max': max(self.times)
            },
            'throughput': {
                'mean': statistics.mean(self.throughputs),
                'median': statistics.median(self.throughputs),
                'stdev': statistics.stdev(self.throughputs) if len(self.throughputs) > 1 else 0,
                'min': min(self.throughputs),
                'max': max(self.throughputs)
            },
            'latency': {
                'mean': statistics.mean(self.latencies) if self.latencies else 0,
                'median': statistics.median(self.latencies) if self.latencies else 0,
                'stdev': statistics.stdev(self.latencies) if len(self.latencies) > 1 else 0,
                'min': min(self.latencies) if self.latencies else 0,
                'max': max(self.latencies) if self.latencies else 0
            }
        }

def print_results_table(all_results):
    """Print results in formatted table"""
    print("\n" + "="*120)
    print("📈 VPN PERFORMANCE COMPARISON")
    print("="*120)
    
    print(f"\n{'VPN Type':<20} {'Trials':<8} {'Transfer Time (s)':<20} {'Throughput (KB/s)':<20} {'RTT (ms)':<15}")
    print(f"{'':20} {'':8} {'Mean ± StdDev':<20} {'Mean ± StdDev':<20} {'Mean ± StdDev':<15}")
    print("-"*120)
    
    for result in all_results:
        if result:
            tt = result['transfer_time']
            tp = result['throughput']
            lat = result['latency']
            
            print(f"{result['vpn_name']:<20} {result['trials']:<8} "
                  f"{tt['mean']:.3f} ± {tt['stdev']:.3f}      "
                  f"{tp['mean']:.0f} ± {tp['stdev']:.0f}        "
                  f"{lat['mean']:.1f} ± {lat['stdev']:.1f}")
    
    print("="*120)

def save_results(all_results):
    """Save results to JSON file"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'configuration': {
            'remote_host': REMOTE_HOST,
            'file_size_kb': 170,
            'num_trials': NUM_TRIALS,
            'file_url': FILE_URL
        },
        'results': all_results
    }
    
    with open(RESULTS_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Results saved to: {RESULTS_FILE}")

def main():
    print("\n" + "="*120)
    print("🔬 VPN PERFORMANCE MEASUREMENT TOOL")
    print("="*120)
    print(f"Remote Host: {REMOTE_HOST}")
    print(f"File Size: 170 KB (Alice in Wonderland)")
    print(f"Trials per VPN: {NUM_TRIALS}")
    print(f"Results File: {RESULTS_FILE}")
    print("="*120)
    
    # Define VPN configurations to test
    vpn_configs = [
        VPNMeasurement("Baseline (No VPN)", "Direct connection, no encryption"),
        VPNMeasurement("GRE Tunnel", "GRE encapsulation only, no encryption"),
        VPNMeasurement("GRE + IPSec", "GRE with AES-256 encryption"),
        VPNMeasurement("WireGuard", "Modern VPN with ChaCha20 encryption"),
        VPNMeasurement("OpenVPN", "Mature VPN with AES-256 encryption"),
    ]
    
    all_results = []
    
    # Run measurements for each VPN
    for vpn in vpn_configs:
        print(f"\n⏳ Preparing to test: {vpn.vpn_name}")
        print(f"   Make sure the tunnel is UP and remote host is reachable")
        print(f"   Press ENTER to start, or Ctrl+C to skip...")
        
        try:
            input()
            if vpn.run_trials():
                stats = vpn.get_statistics()
                all_results.append(stats)
            else:
                print(f"   ⚠️  Skipping {vpn.vpn_name} - no successful trials")
                all_results.append(None)
        except KeyboardInterrupt:
            print(f"\n   ⏭️  Skipping {vpn.vpn_name}")
            all_results.append(None)
    
    # Print summary
    print_results_table(all_results)
    
    # Save results
    save_results(all_results)
    
    print("\n✅ Measurement complete!")
    print(f"📊 Open {RESULTS_FILE} to view detailed results")

if __name__ == "__main__":
    main()
