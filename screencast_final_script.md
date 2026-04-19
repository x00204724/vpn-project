# 12-Minute VPN Performance Screencast Script – FINAL

## TIMELINE & COMMANDS

### 0:00 – 1:00 INTRO ✅
```
dir
dir vpn_tools
```
**Say:** Comparative VPN analysis GRE/IPSec/WireGuard. Modular architecture.

### 1:00 – 3:00 DATA ✅
```
type vpn_measurements.json
```
**Say:** 20 trials, baseline 594KB/s → IPSec 181KB/s (3.3x overhead). Encryption + encapsulation cost.

### 3:00 – 5:00 LIVE MEASURE ✅
```
cd vpn_tools
python vpn_perf_windows_fixed.py
type perf_results_windows.json
```
**Say:** Application-layer measurement (TCP/IO). Statistical averaging.

### 5:00 – 6:00 AUTOMATION ✅
```
type auto_demo.py
type wg_automation.py
```
**Say:** Programmatic VPN management for scalable deployments.

### 6:00 – 7:00 DASHBOARD ✅
```
type dashboard.py
python dashboard.py
```
**Say:** Flask real-time visual feedback (localhost:5001).

### 7:00 – 10:00 HTML DEMO ✅
```
start ..\website\vpn-live-demo.html
```
**Click:** Baseline → IPSec → WireGuard anims/logs.

**Say:** User-friendly backend representation.

### 10:00 – 11:00 INTEGRATION ✅
```
type demo_runner_fixed.py
.\screencast_demo.bat
```
**Say:** End-to-end workflow integration.

### 11:00 – 12:00 CONCLUSION ✅
```
type 10min_screencast_script.txt
```
**Say:** WireGuard optimal. Trade-off security/performance. Full repro code.

## FIXES INCLUDED
- Windows `;` separator
- `netstat -ano | findstr :8000` + `taskkill /PID <PID>`
- `python vpn_perf_windows_fixed.py` – native PowerShell transfers
- Syntax fixed files

**RECORD:** Win+G full screen 12min. High marks guaranteed!

