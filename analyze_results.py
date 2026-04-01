#!/usr/bin/env python3
"""
VPN Measurement Statistics Calculator
Processes measurement data and generates statistical analysis
"""

import json
import statistics
import csv
from pathlib import Path

def load_json_results(filename="vpn_measurements.json"):
    """Load results from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return None

def load_csv_results(filename="vpn_measurements.csv"):
    """Load results from CSV file"""
    results = {}
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                vpn_type = row['VPN_Type']
                
                if vpn_type not in results:
                    results[vpn_type] = {
                        'transfer_times': [],
                        'throughputs': [],
                        'latencies': []
                    }
                
                # Only add if data is filled in
                if row['Transfer_Time_Seconds']:
                    results[vpn_type]['transfer_times'].append(float(row['Transfer_Time_Seconds']))
                if row['Throughput_KB_s']:
                    results[vpn_type]['throughputs'].append(float(row['Throughput_KB_s']))
                if row['RTT_Latency_ms']:
                    results[vpn_type]['latencies'].append(float(row['RTT_Latency_ms']))
        
        return results
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return None

def calculate_stats(data_list):
    """Calculate statistics for a list of values"""
    if not data_list:
        return None
    
    return {
        'count': len(data_list),
        'mean': statistics.mean(data_list),
        'median': statistics.median(data_list),
        'stdev': statistics.stdev(data_list) if len(data_list) > 1 else 0,
        'min': min(data_list),
        'max': max(data_list),
        'range': max(data_list) - min(data_list)
    }

def print_detailed_stats(results):
    """Print detailed statistics for each VPN type"""
    print("\n" + "="*140)
    print("📊 DETAILED VPN PERFORMANCE STATISTICS")
    print("="*140)
    
    for vpn_type in sorted(results.keys()):
        data = results[vpn_type]
        
        print(f"\n🔹 {vpn_type.upper()}")
        print("-"*140)
        
        # Transfer Time Stats
        if data['transfer_times']:
            tt_stats = calculate_stats(data['transfer_times'])
            print(f"  Transfer Time (seconds):")
            print(f"    Mean:     {tt_stats['mean']:.4f}s")
            print(f"    Median:   {tt_stats['median']:.4f}s")
            print(f"    StdDev:   {tt_stats['stdev']:.4f}s")
            print(f"    Min:      {tt_stats['min']:.4f}s")
            print(f"    Max:      {tt_stats['max']:.4f}s")
            print(f"    Range:    {tt_stats['range']:.4f}s")
            print(f"    Trials:   {tt_stats['count']}")
        
        # Throughput Stats
        if data['throughputs']:
            tp_stats = calculate_stats(data['throughputs'])
            print(f"\n  Throughput (KB/s):")
            print(f"    Mean:     {tp_stats['mean']:.1f} KB/s")
            print(f"    Median:   {tp_stats['median']:.1f} KB/s")
            print(f"    StdDev:   {tp_stats['stdev']:.1f} KB/s")
            print(f"    Min:      {tp_stats['min']:.1f} KB/s")
            print(f"    Max:      {tp_stats['max']:.1f} KB/s")
            print(f"    Range:    {tp_stats['range']:.1f} KB/s")
        
        # Latency Stats
        if data['latencies']:
            lat_stats = calculate_stats(data['latencies'])
            print(f"\n  Latency / RTT (ms):")
            print(f"    Mean:     {lat_stats['mean']:.2f}ms")
            print(f"    Median:   {lat_stats['median']:.2f}ms")
            print(f"    StdDev:   {lat_stats['stdev']:.2f}ms")
            print(f"    Min:      {lat_stats['min']:.2f}ms")
            print(f"    Max:      {lat_stats['max']:.2f}ms")
            print(f"    Range:    {lat_stats['range']:.2f}ms")

def print_comparison_table(results):
    """Print comparison table"""
    print("\n" + "="*140)
    print("📈 VPN PERFORMANCE COMPARISON TABLE")
    print("="*140)
    
    print(f"\n{'VPN Type':<20} {'Transfer Time (s)':<25} {'Throughput (KB/s)':<25} {'Latency (ms)':<20}")
    print(f"{'':20} {'Mean ± StdDev':<25} {'Mean ± StdDev':<25} {'Mean ± StdDev':<20}")
    print("-"*140)
    
    for vpn_type in sorted(results.keys()):
        data = results[vpn_type]
        
        tt_stats = calculate_stats(data['transfer_times']) if data['transfer_times'] else None
        tp_stats = calculate_stats(data['throughputs']) if data['throughputs'] else None
        lat_stats = calculate_stats(data['latencies']) if data['latencies'] else None
        
        tt_str = f"{tt_stats['mean']:.3f} ± {tt_stats['stdev']:.3f}" if tt_stats else "N/A"
        tp_str = f"{tp_stats['mean']:.0f} ± {tp_stats['stdev']:.0f}" if tp_stats else "N/A"
        lat_str = f"{lat_stats['mean']:.1f} ± {lat_stats['stdev']:.1f}" if lat_stats else "N/A"
        
        print(f"{vpn_type:<20} {tt_str:<25} {tp_str:<25} {lat_str:<20}")
    
    print("="*140)

def print_overhead_analysis(results):
    """Calculate and print overhead compared to baseline"""
    print("\n" + "="*140)
    print("⚡ ENCRYPTION OVERHEAD ANALYSIS")
    print("="*140)
    
    if 'Baseline (No VPN)' not in results:
        print("⚠️  Baseline data not available for comparison")
        return
    
    baseline_data = results['Baseline (No VPN)']
    baseline_tt = calculate_stats(baseline_data['transfer_times'])
    baseline_tp = calculate_stats(baseline_data['throughputs'])
    
    if not baseline_tt or not baseline_tp:
        print("⚠️  Baseline data incomplete")
        return
    
    print(f"\nBaseline (No VPN) Reference:")
    print(f"  Transfer Time: {baseline_tt['mean']:.3f}s")
    print(f"  Throughput:    {baseline_tp['mean']:.0f} KB/s")
    print("-"*140)
    
    for vpn_type in sorted(results.keys()):
        if vpn_type == 'Baseline (No VPN)':
            continue
        
        data = results[vpn_type]
        tt_stats = calculate_stats(data['transfer_times']) if data['transfer_times'] else None
        tp_stats = calculate_stats(data['throughputs']) if data['throughputs'] else None
        
        if tt_stats and tp_stats:
            time_overhead = ((tt_stats['mean'] - baseline_tt['mean']) / baseline_tt['mean']) * 100
            throughput_reduction = ((baseline_tp['mean'] - tp_stats['mean']) / baseline_tp['mean']) * 100
            
            print(f"\n{vpn_type}:")
            print(f"  Time Overhead:        {time_overhead:+.1f}%")
            print(f"  Throughput Reduction: {throughput_reduction:.1f}%")
            print(f"  Efficiency:           {(100 - throughput_reduction):.1f}%")

def generate_html_table(results):
    """Generate HTML table for website"""
    html = """
<table>
    <thead>
        <tr>
            <th>VPN Technology</th>
            <th>Transfer Time (s)</th>
            <th>Throughput (KB/s)</th>
            <th>Latency (ms)</th>
            <th>Trials</th>
        </tr>
    </thead>
    <tbody>
"""
    
    for vpn_type in sorted(results.keys()):
        data = results[vpn_type]
        
        tt_stats = calculate_stats(data['transfer_times']) if data['transfer_times'] else None
        tp_stats = calculate_stats(data['throughputs']) if data['throughputs'] else None
        lat_stats = calculate_stats(data['latencies']) if data['latencies'] else None
        
        if tt_stats:
            tt_str = f"{tt_stats['mean']:.3f} ± {tt_stats['stdev']:.3f}"
            tp_str = f"{tp_stats['mean']:.0f} ± {tp_stats['stdev']:.0f}" if tp_stats else "N/A"
            lat_str = f"{lat_stats['mean']:.1f} ± {lat_stats['stdev']:.1f}" if lat_stats else "N/A"
            
            html += f"""        <tr>
            <td><strong>{vpn_type}</strong></td>
            <td>{tt_str}</td>
            <td>{tp_str}</td>
            <td>{lat_str}</td>
            <td>{tt_stats['count']}</td>
        </tr>
"""
    
    html += """    </tbody>
</table>
"""
    return html

def main():
    print("\n" + "="*140)
    print("📊 VPN MEASUREMENT STATISTICS CALCULATOR")
    print("="*140)
    
    # Try loading from JSON first, then CSV
    results = load_json_results()
    if not results:
        print("\n⏳ JSON file not found, trying CSV...")
        results = load_csv_results()
    
    if not results:
        print("❌ No measurement data found!")
        return
    
    # Extract results if from JSON format
    if 'results' in results:
        results = results['results']
    
    # Convert JSON format to CSV format if needed
    if results and isinstance(results[0], dict) and 'transfer_time' in results[0]:
        converted = {}
        for result in results:
            if result:
                vpn_name = result['vpn_name']
                converted[vpn_name] = {
                    'transfer_times': [result['transfer_time']['mean']],
                    'throughputs': [result['throughput']['mean']],
                    'latencies': [result['latency']['mean']]
                }
        results = converted
    
    # Print analysis
    print_detailed_stats(results)
    print_comparison_table(results)
    print_overhead_analysis(results)
    
    # Generate HTML
    html = generate_html_table(results)
    print("\n" + "="*140)
    print("📄 HTML TABLE (for website):")
    print("="*140)
    print(html)
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
