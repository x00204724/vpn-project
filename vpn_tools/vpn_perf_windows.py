#!/usr/bin/env python3
    \"\"\"Windows VPN Performance Measurement - No wget needed\"\"\"
import subprocess
import time
import json
from datetime import datetime
from statistics import mean

ALICE_FILE = 'AliceInWonderland.txt'
PORT = 8000

class WindowsPerfMeasure:
    def measure_baseline(self, trials=5):
        print('\n=== BASELINE (LOCAL) MEASUREMENT ===')
        print('[*] Starting HTTP server...')
        server = subprocess.Popen(['python', '-m', 'http.server', str(PORT)])
        time.sleep(1)
        
        times = []
        for i in range(trials):
            start = time.perf_counter()
            try:
                cmd = f'powershell -c "Invoke-WebRequest -Uri http://localhost:{PORT}/{ALICE_FILE} -OutFile test{{0}}.txt -UseBasicParsing"'
                result = subprocess.run(cmd, shell=True, capture_output=True, timeout=10)
                end = time.perf_counter()
                if result.returncode == 0:
                    times.append(end - start)
                    print(f'Trial {i+1}: {end-start:.3f}s')
                else:
                    print(f'Trial {i+1}: FAILED')
            except:
                print(f'Trial {i+1}: TIMEOUT')
        
        server.terminate()
        
        if times:
            avg = mean(times)
            throughput = 170 / avg  # KB/s
            result = {
                'type': 'baseline_windows',
                'trials': len(times),
                'avg_time_s': avg,
                'throughput_kbs': throughput
            }
            with open('perf_results_windows.json', 'w') as f:
                json.dump([result], f, indent=2)
            print(f'\n[+] Baseline: {avg:.3f}s ({throughput:.1f} KB/s)')
            print('[+] Saved: perf_results_windows.json')
            return result
        return None

if __name__ == '__main__':
    perf = WindowsPerfMeasure()
    perf.measure_baseline(5)

