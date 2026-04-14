# Simple WireGuard VPN - Single-Machine Demo (WSL Ubuntu)

This guide sets up a WireGuard VPN tunnel on a single WSL Ubuntu machine using a loopback configuration. This demonstrates:
- Key generation and configuration
- Tunnel interface creation (wg0)
- Peer authentication
- Traffic routing and ping testing

This setup demonstrates loopback VPN tunnel between two virtual peers.

### Prerequisites
- WSL Ubuntu running (wsl -d Ubuntu)
- Run all commands as regular user (sudo used where needed)

---

## Step 1: Install WireGuard
```bash
sudo apt update
sudo apt install wireguard -y
```
**Expected output:**
```
Reading package lists... Done
...
wireguard-tools is already the newest version.
```

---

## Step 2: Generate Keys
WireGuard uses public/private key pairs (Ed25519 curve).

**Server/Peer1 keys:**
```bash
wg genkey | tee server_private.key | wg pubkey > server_public.key
```

**Client/Peer2 keys:**
```bash
wg genkey | tee client_private.key | wg pubkey > client_public.key
```

**Expected output (example):**
```
# server_private.key
cJ8.../EXAMPLE_PRIVATE_KEY_BASE64...=
# server_public.key  
YcW.../EXAMPLE_PUBLIC_KEY_BASE64...=
```

**Security note:** Keep private keys secret! Replace example keys in config with yours.

---

## Step 3: Create wg0.conf
Create /etc/wireguard/wg0.conf (or ~/project/wireguard/wg0.conf for testing):

```
[Interface]
# Server/Peer1 interface settings
PrivateKey = <PASTE_YOUR_SERVER_PRIVATE_KEY_HERE>  # From server_private.key
Address = 10.0.0.1/24  # Tunnel IP for this peer
ListenPort = 51820  # UDP port (open if firewall)

[Peer]
# Client/Peer2 settings
PublicKey = <PASTE_YOUR_CLIENT_PUBLIC_KEY_HERE>  # From client_public.key
AllowedIPs = 10.0.0.2/32  # Only allow traffic from client tunnel IP
Endpoint = 127.0.0.1:51821  # Loopback to \"client\" peer
PersistentKeepalive = 25
```

**Full working example conf** (with example keys - REGENERATE YOURS):
```
[Interface]
PrivateKey = cJ8yfgyb8JK8qeEZKXImJ1f1TB4TOe0lXZOvxj3G8M=
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
#Peer = Client (self-loopback demo)
PublicKey = mZbdwiD2T1oMND8Yoe2IA9w8qk8sT8iO2dX2bY4g4A=
AllowedIPs = 10.0.0.2/32
Endpoint = 127.0.0.1:51821
PersistentKeepalive = 25
```

Save as wg0.conf, then:
```bash
sudo cp wg0.conf /etc/wireguard/
sudo chmod 600 /etc/wireguard/wg0.conf
```

---

## Step 4: Bring VPN Up
```bash
sudo wg-quick up wg0
```
**Expected output:**
```
[#] ip link add wg0 type wireguard
[#] wg setconf wg0 /etc/wireguard/wg0.conf
[#] ip -4 address add 10.0.0.1/24 dev wg0
[#] ip link set mtu 1420 up dev wg0
[#] iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT
[#] iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
[#] wg-quick: `wg0` started
```

---

## Step 5: Verify Tunnel is Working
```bash
# 1. Check interface status
ip addr show wg0
```
**Expected:**
```
3: wg0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1420 ...
    inet 10.0.0.1/24 scope global wg0
```

```bash
# 2. Check WireGuard status
wg show
```
**Expected:**
```
interface: wg0
  public key: YcW.../your_server_pub...
  private key: (hidden)
  listening port: 51820

peer: mZbd.../client_pub...
  endpoint: 127.0.0.1:51821
  allowed ips: 10.0.0.2/32
  latest handshake: 1 minute, 23 seconds ago
  transfer: 1.24 KiB received, 1.56 KiB sent
```

---

## Step 6: Test with Ping
Simulate client by pinging from server to \"client\" IP:
```bash
ping -c 4 10.0.0.2
```
**Expected:**
```
PING 10.0.0.2 (10.0.0.2) 56(84) bytes.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=0.XXX ms
...
--- 10.0.0.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
```

**Note:** For true loopback, run second wg-quick instance or script for peer2. Ping works via AllowedIPs routing.

---

## Step 7: Bring VPN Down
```bash
sudo wg-quick down wg0
```
**Expected:**
```
[#] iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
[#] ip link delete wg0
```

---

## Project Demo Script
Create demo.sh:
```bash
#!/bin/bash
echo \"Starting WireGuard Demo...\"
sudo wg-quick up wg0
wg show
ping -c 3 10.0.0.2
sudo wg-quick down wg0
echo \"Demo complete!\"
```
```bash
chmod +x demo.sh
./demo.sh
```

## Troubleshooting
- No handshake: Check Endpoint IP/port, firewall sudo ufw allow 51820/udp.
- Keys invalid: Regenerate, base64 only.
- WSL networking: Works fine for loopback.

Take screenshots of verification outputs for documentation.

