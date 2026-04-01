# 📊 MANUAL VPN MEASUREMENT GUIDE (GNS3 Console)

## QUICK START - 30 MINUTES

### Step 1: Open GNS3 Console to Local Ubuntu (192.168.1.33)

In GNS3:
1. Right-click on ubuntunew-9 (local Ubuntu VM)
2. Select "Console"
3. Login: ubuntu / ubuntu

### Step 2: Verify Connectivity

```bash
# Test ping to remote Ubuntu through tunnel
ping -c 5 192.168.2.33

# Should see responses like:
# 64 bytes from 192.168.2.33: icmp_seq=1 ttl=63 time=12.5 ms
```

**Record RTT values from ping output**

### Step 3: Start HTTP Server on Remote Ubuntu

In GNS3:
1. Right-click on ubuntunew-1 (remote Ubuntu VM)
2. Select "Console"
3. Login: ubuntu / ubuntu

```bash
# Start HTTP server
cd /home/ubuntu
python3 -m http.server 8000

# Should see:
# Serving HTTP on 0.0.0.0 port 8000
```

**Keep this terminal open**

### Step 4: Test File Download (Local Ubuntu)

Back on local Ubuntu console:

```bash
# Test download
time wget http://192.168.2.33:8000/AliceInWonderland.txt -O /tmp/test.txt

# Output will show:
# real    0m0.287s
# user    0m0.001s
# sys     0m0.002s
```

**Record the "real" time**

### Step 5: Run 20 Trials

Repeat the download 20 times and record each time:

```bash
# Trial 1
time wget http://192.168.2.33:8000/AliceInWonderland.txt -O /tmp/test.txt

# Trial 2
time wget http://192.168.2.33:8000/AliceInWonderland.txt -O /tmp/test.txt

# ... repeat 18 more times
```

---

## 📋 DATA RECORDING SHEET

Copy this and fill in your measurements:

```
GRE TUNNEL MEASUREMENTS (20 Trials)
File: AliceInWonderland.txt (170 KB)
Date: _______________

Trial | Transfer Time (s) | Notes
------|-------------------|-------
  1   | _________________ |
  2   | _________________ |
  3   | _________________ |
  4   | _________________ |
  5   | _________________ |
  6   | _________________ |
  7   | _________________ |
  8   | _________________ |
  9   | _________________ |
 10   | _________________ |
 11   | _________________ |
 12   | _________________ |
 13   | _________________ |
 14   | _________________ |
 15   | _________________ |
 16   | _________________ |
 17   | _________________ |
 18   | _________________ |
 19   | _________________ |
 20   | _________________ |

STATISTICS:
Mean:     _________________ seconds
Min:      _________________ seconds
Max:      _________________ seconds
Range:    _________________ seconds

Throughput (170 KB / time):
Mean:     _________________ KB/s
Min:      _________________ KB/s
Max:      _________________ KB/s

Latency (from ping):
Mean RTT: _________________ ms
```

---

## ⚡ FASTER METHOD (10 minutes)

If you want to speed this up, create a bash script on the Ubuntu VM:

```bash
# On local Ubuntu console, create script:
cat > /tmp/measure.sh << 'EOF'
#!/bin/bash
for i in {1..20}; do
  echo "Trial $i:"
  time wget http://192.168.2.33:8000/AliceInWonderland.txt -O /tmp/test.txt 2>&1 | grep real
  sleep 1
done
EOF

# Make executable
chmod +x /tmp/measure.sh

# Run it
/tmp/measure.sh
```

This will run all 20 trials automatically and show times.

---

## 📝 EXAMPLE OUTPUT

```
Trial 1:
real    0m0.287s

Trial 2:
real    0m0.291s

Trial 3:
real    0m0.289s

...

Trial 20:
real    0m0.285s
```

---

## 🎯 WHAT TO DO NOW

1. **Open GNS3 console to local Ubuntu**
2. **Verify ping works to 192.168.2.33**
3. **Start HTTP server on remote Ubuntu**
4. **Run the bash script (faster method)**
5. **Record all 20 times**
6. **Calculate mean/min/max**
7. **Report results**

---

## ✅ EXPECTED RESULTS

For GRE tunnel (no encryption):
- Transfer time: 0.28-0.35 seconds
- Throughput: 480-600 KB/s
- Latency: 10-20ms

---

## 📊 ONCE YOU HAVE DATA

1. Fill in the CSV: vpn_measurements.csv
2. Run: python analyze_results.py
3. Get HTML table for website
4. Update website with real data

---

**Start now! You've got this! 🚀**
