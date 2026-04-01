# 🚀 HOW TO RUN VPN MEASUREMENTS IN GNS3

## QUICK START (5 minutes)

### Step 1: SSH into Local Ubuntu VM (Site A)
```bash
# From GNS3 console or SSH
ssh ubuntu@192.168.1.33
# Password: ubuntu (or whatever you set)
```

### Step 2: Copy Measurement Script
```bash
# Copy the script to the Ubuntu VM
# Option A: Use SCP from Windows
scp measure_vpn_gns3.py ubuntu@192.168.1.33:/home/ubuntu/

# Option B: Create it manually
nano measure_vpn_gns3.py
# Paste the script content
# Ctrl+X, Y, Enter to save
```

### Step 3: Make Script Executable
```bash
chmod +x measure_vpn_gns3.py
```

### Step 4: Verify Remote Ubuntu is Ready
```bash
# SSH into remote Ubuntu (Site B)
ssh ubuntu@192.168.2.33

# Start HTTP server
cd /home/ubuntu
python3 -m http.server 8000

# Leave this running in background or new terminal
```

### Step 5: Run Measurement
```bash
# Back on local Ubuntu (192.168.1.33)
python3 measure_vpn_gns3.py

# When prompted, press ENTER to start
# Script runs 20 trials automatically
# Results print to console
```

### Step 6: View Results
```bash
# Results saved to JSON
cat /tmp/vpn_measurements.json

# Copy output and save to Windows
```

---

## DETAILED STEPS

### On Remote Ubuntu (192.168.1.33 - Site B)

1. **Start HTTP Server**
```bash
cd /home/ubuntu
python3 -m http.server 8000
```

Keep this running. You should see:
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

### On Local Ubuntu (192.168.1.33 - Site A)

1. **Verify Connectivity**
```bash
# Test ping through tunnel
ping -c 1 192.168.2.33

# Should respond with RTT ~10-50ms
```

2. **Test File Download**
```bash
# Test downloading the file
wget http://192.168.2.33:8000/AliceInWonderland.txt -O /tmp/test.txt

# Should complete in <1 second
```

3. **Run Measurement Script**
```bash
python3 measure_vpn_gns3.py
```

4. **Follow Prompts**
```
Press ENTER to start...
Trial 1: 0.287s | 592 KB/s | RTT: 12.5ms
Trial 2: 0.291s | 584 KB/s | RTT: 13.2ms
...
Trial 20: 0.289s | 588 KB/s | RTT: 12.8ms
```

---

## EXPECTED RESULTS

### GRE Tunnel (No Encryption)
- Transfer Time: 0.28-0.35 seconds
- Throughput: 480-600 KB/s
- Latency: 10-20ms

---

## TROUBLESHOOTING

### "Connection refused"
```
❌ HTTP server not running on remote
✅ Fix: Start HTTP server on 192.168.2.33
```

### "Destination unreachable"
```
❌ Tunnel not working
✅ Fix: Check tunnel is UP on R1 & R2
✅ Fix: Check routing
```

### "wget: command not found"
```
❌ wget not installed
✅ Fix: sudo apt install wget
```

### "Python3 not found"
```
❌ Python not installed
✅ Fix: sudo apt install python3
```

---

## GETTING RESULTS BACK TO WINDOWS

### Option 1: Copy JSON Output
```bash
# On Ubuntu, display results
cat /tmp/vpn_measurements.json

# Copy the entire JSON output
# Paste into a file on Windows: vpn_measurements.json
```

### Option 2: Use SCP
```powershell
# On Windows PowerShell
scp ubuntu@192.168.1.33:/tmp/vpn_measurements.json .
```

### Option 3: Email/Paste
```bash
# On Ubuntu
cat /tmp/vpn_measurements.json | xclip -selection clipboard

# Then paste into Windows file
```

---

## NEXT STEPS

1. ✅ Run GRE measurement (today)
2. ✅ Get results back to Windows
3. ⏳ Configure GRE+IPSec on routers
4. ⏳ Run GRE+IPSec measurement
5. ⏳ Install WireGuard on Ubuntu VMs
6. ⏳ Run WireGuard measurement

---

## QUICK REFERENCE

| Command | Purpose |
|---------|---------|
| `ssh ubuntu@192.168.1.33` | SSH to local Ubuntu |
| `ssh ubuntu@192.168.2.33` | SSH to remote Ubuntu |
| `python3 -m http.server 8000` | Start HTTP server |
| `python3 measure_vpn_gns3.py` | Run measurements |
| `cat /tmp/vpn_measurements.json` | View results |
| `ping -c 1 192.168.2.33` | Test connectivity |
| `wget http://192.168.2.33:8000/AliceInWonderland.txt` | Test download |

---

Good luck! 🚀
