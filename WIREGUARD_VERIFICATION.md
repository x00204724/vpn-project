# WireGuard VPN Verification Guide

Run these commands in your WSL Ubuntu terminal to confirm WireGuard VPN is fully working.

## 1. Check WireGuard Interface Status
**Command:**
```bash
sudo wg show
```

**Expected Output:**
```
interface: wg0
  public key: ABC123xyz...=  (your server's public key)
  private key: (hidden)
  listening port: 51820

peer: DEF456uvw...=  (client's public key)
  endpoint: 127.0.0.1:51821
  allowed ips: 10.0.0.2/32
  latest handshake: 2 minutes, 15 seconds ago (Recent handshake confirms encryption active)
  transfer: 5.23 KiB received, 7.12 KiB sent
```

**What it means:** Shows tunnel interface wg0 is running, peers connected, data transferred. Recent handshake confirms encryption active and tunnel live.

---

## 2. Check IP Address Assignment
**Command:**
```bash
ip addr show wg0
```

**Expected Output:**
```
4: wg0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.0.0.1/24 scope global wg0
       valid_lft forever preferred_lft forever
```

**What it means:** UP,LOWER_UP = interface active. 10.0.0.1/24 = correct tunnel IP assigned.

---

## 3. Ping Test (Tunnel Connectivity)
**Command:**
```bash
ping -c 4 10.0.0.2
```

**Expected Output:**
```
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=0.45 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.32 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.28 ms
64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.41 ms

--- 10.0.0.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
```

**What it means:** 0% packet loss means tunnel routing works. Low latency expected for loopback.

---

## 4. Check Active Interfaces
**Command:**
```bash
ip link show | grep wg
```

**Expected Output:**
```
4: wg0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1420 ...
```

**What it means:** Confirms wg0 interface exists and is UP.

---

## 5. Check Routing Table
**Command:**
```bash
ip route show table main | grep wg0
```

**Expected Output:**
```
10.0.0.0/24 dev wg0 proto kernel scope link src 10.0.0.1 
```

**What it means:** Traffic to 10.0.0.0/24 subnet routes through tunnel.

## VPN Status Confirmation
- wg show: handshake recent - Encryption active, peers communicating
- ip addr show wg0: UP + IP - Interface configured correctly
- ping 10.0.0.2: 0% loss - Tunnel connectivity perfect
- Data transfer in wg show - Real encrypted traffic flowing

If all pass, WireGuard VPN is fully operational.

## Notes
If any check fails, try restarting: sudo wg-quick down wg0 && sudo wg-quick up wg0

