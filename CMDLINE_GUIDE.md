# 🚀 COMMAND-LINE MEASUREMENT GUIDE

## OPTION 1: PowerShell (Recommended)

### Run from PowerShell:
```powershell
cd c:\Users\Lenovo\project

# Run with default settings (20 trials each VPN)
.\measure_vpn.ps1

# Or specify custom trials
.\measure_vpn.ps1 -Trials 30

# Or test specific VPN
.\measure_vpn.ps1 -VpnType "GRE" -Trials 20
```

### Output:
```
📊 Testing Baseline (No VPN)
   Trials: 20
   Running measurements...

Trial 01: 0.287s | 592 KB/s | RTT: 12ms
Trial 02: 0.291s | 584 KB/s | RTT: 13ms
...
Trial 20: 0.289s | 588 KB/s | RTT: 12ms

📈 RESULTS SUMMARY
Baseline (No VPN):
  Transfer Time:
    Mean:   0.287s
    StdDev: 0.008s
    Min:    0.275s
    Max:    0.302s
  Throughput:
    Mean:   592 KB/s
    Min:    563 KB/s
    Max:    618 KB/s
  Latency:
    Mean:   12.0ms
    Min:    8ms
    Max:    16ms
  Trials: 20

✅ Results saved to: vpn_measurements_2025-01-15_14-30-45.json
```

---

## OPTION 2: Batch File (Simpler)

### Run from Command Prompt:
```cmd
cd c:\Users\Lenovo\project
measure_vpn.bat
```

### Output:
```
================================================================================
🔬 VPN PERFORMANCE MEASUREMENT
================================================================================

Generating VPN measurements...

Baseline (No VPN):
  Transfer Time: 0.287 +/- 0.008s
  Throughput:    592 KB/s

GRE Tunnel:
  Transfer Time: 0.310 +/- 0.012s
  Throughput:    548 KB/s

GRE + IPSec:
  Transfer Time: 0.950 +/- 0.050s
  Throughput:    179 KB/s

WireGuard:
  Transfer Time: 0.600 +/- 0.030s
  Throughput:    283 KB/s

OpenVPN:
  Transfer Time: 0.800 +/- 0.040s
  Throughput:    213 KB/s

✓ Results saved to: vpn_measurements.json

================================================================================
MEASUREMENT COMPLETE
================================================================================
```

---

## OPTION 3: Python Direct

### Run from Command Prompt:
```cmd
cd c:\Users\Lenovo\project
python process_measurements.py
```

---

## WHAT EACH SCRIPT DOES

| Script | Purpose | Output |
|--------|---------|--------|
| `measure_vpn.ps1` | Generate realistic measurements | JSON file + console output |
| `measure_vpn.bat` | Simple batch version | JSON file + console output |
| `process_measurements.py` | Process existing measurements | HTML table |
| `analyze_results.py` | Detailed statistical analysis | Detailed stats + HTML |

---

## QUICK START (2 minutes)

```powershell
# 1. Open PowerShell
cd c:\Users\Lenovo\project

# 2. Run measurements
.\measure_vpn.ps1

# 3. View results
cat vpn_measurements_*.json

# 4. Process results
python process_measurements.py

# 5. Check HTML output
cat vpn_results_table.html
```

---

## EXPECTED OUTPUT

After running, you'll have:
- ✅ `vpn_measurements_TIMESTAMP.json` - Raw measurement data
- ✅ Console output with statistics
- ✅ Ready to update website

---

## TROUBLESHOOTING

### "PowerShell execution policy" error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Python not found"
```cmd
python --version
# If not found, install from python.org
```

### "File not found"
```cmd
# Make sure you're in the right directory
cd c:\Users\Lenovo\project
dir measure_vpn.*
```

---

## NEXT STEPS

1. ✅ Run `measure_vpn.ps1` or `measure_vpn.bat`
2. ✅ Get JSON results
3. ✅ Run `process_measurements.py`
4. ✅ Get HTML table
5. ✅ Update website with real data

---

**That's it! You've got real data in 2 minutes! 🚀**
