#!/usr/bin/env python3
"""
Process manual VPN measurements and generate statistics
"""

import json
import statistics
from pathlib import Path

def process_measurements(json_file):
    """Load measurements from JSON and calculate statistics"""
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    session = data['measurement_session']
    trials = data['trials']
    
    # Extract transfer times
    times = [trial['transfer_time_seconds'] for trial in trials]
    
    # Calculate statistics
    stats = {
        'vpn_type': session['vpn_type'],
        'trials': len(times),
        'file_size_kb': session['file_size_kb'],
        'transfer_time': {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times)
        },
        'throughput': {
            'mean': (session['file_size_kb'] / statistics.mean(times)),
            'min': (session['file_size_kb'] / max(times)),
            'max': (session['file_size_kb'] / min(times))
        }
    }
    
    return stats

def print_results(stats):
    """Print formatted results"""
    print("\n" + "="*80)
    print(f"📊 {stats['vpn_type'].upper()} - MEASUREMENT RESULTS")
    print("="*80)
    
    tt = stats['transfer_time']
    tp = stats['throughput']
    
    print(f"\nTransfer Time (seconds):")
    print(f"  Mean:     {tt['mean']:.4f}s")
    print(f"  Median:   {tt['median']:.4f}s")
    print(f"  StdDev:   {tt['stdev']:.4f}s")
    print(f"  Min:      {tt['min']:.4f}s")
    print(f"  Max:      {tt['max']:.4f}s")
    print(f"  Range:    {tt['max'] - tt['min']:.4f}s")
    
    print(f"\nThroughput (KB/s):")
    print(f"  Mean:     {tp['mean']:.1f} KB/s")
    print(f"  Min:      {tp['min']:.1f} KB/s")
    print(f"  Max:      {tp['max']:.1f} KB/s")
    
    print(f"\nTrials: {stats['trials']}")
    print(f"File Size: {stats['file_size_kb']} KB")
    print("="*80)

def generate_html_row(stats):
    """Generate HTML table row"""
    tt = stats['transfer_time']
    tp = stats['throughput']
    
    html = f"""        <tr>
            <td><strong>{stats['vpn_type']}</strong></td>
            <td>{tt['mean']:.3f} ± {tt['stdev']:.3f}</td>
            <td>{tp['mean']:.0f} ± {(tp['max']-tp['min'])/2:.0f}</td>
            <td>{stats['trials']}</td>
        </tr>
"""
    return html

def main():
    print("\n" + "="*80)
    print("📈 VPN MEASUREMENT PROCESSOR")
    print("="*80)
    
    # Find all measurement JSON files
    json_files = list(Path('.').glob('*_measurements_template.json'))
    
    if not json_files:
        print("❌ No measurement files found!")
        print("   Expected: *_measurements_template.json")
        return
    
    all_stats = []
    
    for json_file in sorted(json_files):
        print(f"\n⏳ Processing: {json_file}")
        try:
            stats = process_measurements(json_file)
            all_stats.append(stats)
            print_results(stats)
        except Exception as e:
            print(f"❌ Error processing {json_file}: {e}")
    
    # Generate HTML table
    print("\n" + "="*80)
    print("📄 HTML TABLE (for website)")
    print("="*80)
    
    html = """<table>
    <thead>
        <tr>
            <th>VPN Technology</th>
            <th>Transfer Time (s)</th>
            <th>Throughput (KB/s)</th>
            <th>Trials</th>
        </tr>
    </thead>
    <tbody>
"""
    
    for stats in all_stats:
        html += generate_html_row(stats)
    
    html += """    </tbody>
</table>
"""
    
    print(html)
    
    # Save HTML
    with open('vpn_results_table.html', 'w') as f:
        f.write(html)
    
    print("\n✅ HTML saved to: vpn_results_table.html")
    print("   Copy this into your website!")

if __name__ == "__main__":
    main()
