#!/usr/bin/env python3
"""
VPN Performance Measurement - GNS3 Ubuntu Version
Run this ON the Ubuntu VMs inside GNS3
"""

import time
import subprocess
import statistics
import json
from datetime import datetime

# Configuration - CHANGE THESE FOR YOUR SETUP
REMOTE_HOST = "192.168.2.33"  # Remote Ubuntu VM IP
LOCAL_HOST = "192.168.1.33"   # Local Ubuntu VM IP
FILE_URL = f"http://{REMOTE_HOST}:8000/AliceInWonderland.txt"
OUTPUT_FILE = "/tmp/test_file.txt"
NUM_TRIALS = 20

def measure_transfer(file_url, output_file, timeout=30):
    """Measure single file transfer using wget"""
    try:
        start_time = time.time()
        
        result = subprocess.run(
            ['wget', '-q', '-O', output_file, file_url],
            capture_output=True,
            timeout=timeout
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            # Get file size
            size_result = subprocess.run(
                ['stat', '-c', '%s', output_file],
                capture_output=True,
                text=True
            )
            file_size_bytes = int(size_result.stdout.strip())
            file_size_kb = file_size_bytes / 1024
            throughput = file_size_kb / elapsed if elapsed > 0 else 0
            
            return elapsed, throughput, file_size_kb
        else:
            return None, None, None
            
    except subprocess.TimeoutExpired:
        return None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

def measure_latency(host):
    """Measure RTT latency using ping"""
    try:
        result = subprocess.run(
            ['ping', '-c', '1', host],
            capture_output=True,
            timeout=5,
            text=True
        )
        
        if 'time=' in result.stdout:
            time_str = result.stdout.split('time=')[1].split(' ')[0]
            return float(time_str)
        else:
            return None
            
    except Exception as e:
        print(f"Ping error: {e}")
        return None

def run_measurement(vpn_name, remote_host, num_trials=NUM_TRIALS):
    """Run measurement trials"""
    print(f"\n📊 Testing {vpn_name}")
    print(f"   Remote: {remote_host}")
    print(f"   Trials: {num_trials}")
    print("-" * 60)
    
    times = []
    throughputs = []
    latencies = []
    file_sizes = []
    
    for trial in range(1, num_trials + 1):
        # Measure latency
        latency = measure_latency(remote_host)
        if latency:
            latencies.append(latency)
        
        # Measure transfer
        transfer_time, throughput, file_size = measure_transfer(
            f"http://{remote_host}:8000/AliceInWonderland.txt",
            OUTPUT_FILE
        )
        
        if transfer_time and throughput:
            times.append(transfer_time)
            throughputs.append(throughput)
            file_sizes.append(file_size)
            
            lat_str = f" | RTT: {latency:.1f}ms" if latency else ""
            print(f"Trial {trial:2d}: {transfer_time:.3f}s | {throughput:.0f} KB/s{lat_str}")
        else:
            print(f"Trial {trial:2d}: ❌ FAILED")
        
        time.sleep(0.5)
    
    if times:
        return {
            'vpn_name': vpn_name,
            'trials': len(times),
            'transfer_time': {
                'mean': statistics.mean(times),
                'stdev': statistics.stdev(times) if len(times) > 1 else 0,
                'min': min(times),
                'max': max(times)
            },
            'throughput': {
                'mean': statistics.mean(throughputs),
                'stdev': statistics.stdev(throughputs) if len(throughputs) > 1 else 0,
                'min': min(throughputs),
                'max': max(throughputs)
            },
            'latency': {
                'mean': statistics.mean(latencies) if latencies else 0,
                'stdev': statistics.stdev(latencies) if len(latencies) > 1 else 0,
                'min': min(latencies) if latencies else 0,
                'max': max(latencies) if latencies else 0
            },
            'file_size_kb': statistics.mean(file_sizes) if file_sizes else 0
        }
    else:
        return None

def main():
    print("\n" + "="*60)
    print("🔬 VPN PERFORMANCE MEASUREMENT (GNS3 Ubuntu)")
    print("="*60)
    print(f"Remote Host: {REMOTE_HOST}")
    print(f"Trials per VPN: {NUM_TRIALS}")
    print("="*60)
    
    results = []
    
    # Test GRE Tunnel (through tunnel)
    print("\n⏳ Testing GRE Tunnel (through tunnel to remote site)")
    print("   Make sure tunnel is UP on both routers")
    input("   Press ENTER to start...")
    
    result = run_measurement("GRE Tunnel", REMOTE_HOST, NUM_TRIALS)
    if result:
        results.append(result)
    
    # Print summary
    print("\n" + "="*60)
    print("📈 RESULTS SUMMARY")
    print("="*60)
    
    for result in results:
        if result:
            tt = result['transfer_time']
            tp = result['throughput']
            lat = result['latency']
            
            print(f"\n{result['vpn_name']}:")
            print(f"  Transfer Time: {tt['mean']:.3f} ± {tt['stdev']:.3f}s")
            print(f"  Throughput:    {tp['mean']:.0f} ± {tp['stdev']:.0f} KB/s")
            print(f"  Latency:       {lat['mean']:.1f} ± {lat['stdev']:.1f}ms")
            print(f"  Trials:        {result['trials']}")
    
    # Save results
    output = {
        'timestamp': datetime.now().isoformat(),
        'results': results
    }
    
    with open('/tmp/vpn_measurements.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n✅ Results saved to: /tmp/vpn_measurements.json")
    print("\n📋 Copy this JSON to your Windows machine for analysis")

if __name__ == "__main__":
    main()
