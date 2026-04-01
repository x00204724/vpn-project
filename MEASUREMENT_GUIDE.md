# 🚀 VPN MEASUREMENT QUICK START

## BEFORE YOU START

### 1. Verify GNS3 Lab is Running
```
✅ R1 and R2 routers UP
✅ GRE Tunnel0 is UP (show interface tunnel0)
✅ Ubuntu VMs running on both sites
✅ HTTP server running on remote Ubuntu (python3 -m http.server 8000)
```

### 2. Verify Connectivity
From your Windows host, test:
```powershell
# Test baseline (direct to local Ubuntu)
ping 192.168.1.33

# Test through tunnel (to remote Ubuntu)
ping 192.168.2.33
```

Both should respond. If not, fix GNS3 connectivity first.

### 3. Prepare Alice File
On remote Ubuntu (192.168.2.33):
```bash
# Download file if not already there
wget https://www.gutenberg.org/cache/epub/11/pg11.txt -O AliceInWonderland.txt

# Start HTTP server
cd /home/ubuntu
python3 -m http.server 8000
```

---

## RUNNING MEASUREMENTS

### Step 1: Open PowerShell
```powershell
cd c:\Users\Lenovo\project
```

### Step 2: Run Python Script
```powershell
python measure_vpn.py
```

### Step 3: Follow Prompts
For each VPN type:
1. Make sure tunnel is UP
2. Press ENTER to start
3. Script runs 20 trials automatically
4. Results print to console

### Step 4: Results Saved
- `vpn_measurements.json` - Detailed results
- `vpn_measurements.csv` - Can import to Excel

---

## TESTING EACH VPN TYPE

### BASELINE (No VPN)
```
✅ Just direct connection
✅ No tunnel needed
✅ Should be fastest
```

### GRE TUNNEL
```
Before testing:
1. Verify tunnel is UP: show interface tunnel0
2. Verify routing: show ip route
3. Test ping: ping 192.168.2.33

If tunnel is DOWN:
- Check R1 & R2 configs
- Verify IP addresses match
- Check Hub1 connectivity
```

### GRE + IPSec
```
Before testing:
1. Configure IPSec on R1 & R2
2. Verify tunnel is UP
3. Test ping through tunnel

If you haven't done IPSec yet:
- Skip this for now
- Come back after configuring IPSec
```

### WireGuard
```
Before testing:
1. Install WireGuard on both Ubuntu VMs
2. Generate keys
3. Configure interfaces
4. Test ping

Installation:
sudo apt update
sudo apt install wireguard wireguard-tools
```

### OpenVPN
```
Before testing:
1. Install OpenVPN on both Ubuntu VMs
2. Generate certificates
3. Configure server/client
4. Test ping

Installation:
sudo apt update
sudo apt install openvpn easy-rsa
```

---

## TROUBLESHOOTING

### "Connection refused" or "Timeout"
```
❌ Remote host not reachable
✅ Fix: Check tunnel is UP, HTTP server running
```

### "Transfer failed"
```
❌ File download failed
✅ Fix: Verify Alice file exists on remote Ubuntu
✅ Fix: Check HTTP server is running (port 8000)
```

### "Ping failed"
```
❌ Can't reach remote host
✅ Fix: Check GRE tunnel is UP
✅ Fix: Check routing on both routers
```

### Script crashes
```
❌ Python error
✅ Fix: Make sure Python 3 is installed
✅ Fix: Make sure curl is available
```

---

## EXPECTED RESULTS

### Baseline (No VPN)
- Transfer time: ~0.3 seconds
- Throughput: ~500+ KB/s
- RTT: ~10-15ms

### GRE Tunnel
- Transfer time: ~0.3-0.4 seconds
- Throughput: ~400-500 KB/s
- RTT: ~12-18ms (slight overhead)

### GRE + IPSec
- Transfer time: ~0.8-1.2 seconds
- Throughput: ~150-200 KB/s
- RTT: ~15-25ms (encryption overhead)

### WireGuard
- Transfer time: ~0.4-0.6 seconds
- Throughput: ~250-400 KB/s
- RTT: ~12-20ms (efficient encryption)

### OpenVPN
- Transfer time: ~0.6-0.9 seconds
- Throughput: ~200-300 KB/s
- RTT: ~15-25ms (heavier encryption)

---

## NEXT STEPS

1. ✅ Run measurements for Baseline & GRE (today)
2. ✅ Record results in CSV
3. ⏳ Configure GRE+IPSec (tomorrow)
4. ⏳ Install WireGuard (tomorrow)
5. ⏳ Install OpenVPN (day 3)

---

## QUESTIONS?

If script fails:
1. Check error message
2. Verify tunnel is UP
3. Verify remote host is reachable
4. Check HTTP server is running
5. Try manual curl: `curl http://192.168.2.33:8000/AliceInWonderland.txt`

Good luck! 🚀
