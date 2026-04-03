# PriTunnel Quick Reference Card

**Project:** VPN Connectivity Analysis  
**Author:** Annit Maria Binu  
**Date:** 2025

---

## Installation (One-Liner)

```bash
sudo apt-get update && sudo apt-get install -y python3 python3-pip libssl-dev libffi-dev git && \
cd /opt && sudo git clone https://github.com/pritunnel/pritunnel.git && \
cd pritunnel && sudo pip3 install -r requirements.txt && \
sudo python3 setup.py install && sudo systemctl enable pritunnel && sudo systemctl start pritunnel
```

---

## Essential Commands

### Service Management

```bash
# Start service
sudo systemctl start pritunnel

# Stop service
sudo systemctl stop pritunnel

# Restart service
sudo systemctl restart pritunnel

# Check status
sudo systemctl status pritunnel

# View logs
sudo tail -f /var/log/pritunnel/pritunnel.log

# Enable on boot
sudo systemctl enable pritunnel
```

### Configuration

```bash
# Edit configuration
sudo nano /etc/pritunnel/pritunnel.conf

# Generate certificates
sudo pritunnel-setup

# Initialize database
sudo pritunnel-init

# Start admin console
sudo pritunnel-admin
```

### Network

```bash
# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# Configure NAT
sudo iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE

# Check routing
ip route show

# Check firewall
sudo ufw status
```

### Client

```bash
# Install client (Linux)
sudo apt-get install pritunnel-client

# Start client
pritunnel-client

# Connect to VPN
pritunnel-client --connect "Corporate VPN"

# Disconnect
pritunnel-client --disconnect

# View status
pritunnel-client --status
```

---

## Configuration Snippets

### Server Configuration

```ini
[server]
listen_address = 0.0.0.0
listen_port = 443
cert_file = /etc/pritunnel/server.crt
key_file = /etc/pritunnel/server.key
vpn_network = 10.8.0.0/24
vpn_gateway = 10.8.0.1
max_clients = 100
thread_pool_size = 4

[security]
tls_version = 1.3
cipher = AES-256-CBC
auth_algorithm = SHA256
enable_encryption = true
enable_compression = true

[logging]
log_level = INFO
log_file = /var/log/pritunnel/pritunnel.log
audit_log = /var/log/pritunnel/audit.log
```

### Firewall Rules (UFW)

```bash
sudo ufw allow 443/tcp
sudo ufw allow 443/udp
sudo ufw allow 8000/tcp
sudo ufw enable
```

### Firewall Rules (iptables)

```bash
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

---

## Performance Testing

### Baseline (No VPN)

```bash
time curl http://192.168.1.33:8000/AliceInWonderland.txt -o baseline.txt
```

### PriTunnel Performance

```bash
# Connect to VPN first
time curl http://10.8.0.1:8000/AliceInWonderland.txt -o pritunnel.txt
```

### 20-Trial Test (Bash)

```bash
for i in {1..20}; do
  start=$(date +%s.%N)
  curl -s http://10.8.0.1:8000/AliceInWonderland.txt -o trial_$i.txt
  end=$(date +%s.%N)
  echo "Trial $i: $(echo "$end - $start" | bc) seconds"
done
```

### 20-Trial Test (PowerShell)

```powershell
$results = @()
for ($i = 1; $i -le 20; $i++) {
    $start = Get-Date
    Invoke-WebRequest http://10.8.0.1:8000/AliceInWonderland.txt -OutFile trial_$i.txt
    $end = Get-Date
    $time = ($end - $start).TotalSeconds
    $results += $time
    Write-Host "Trial $i : $time seconds"
}
$mean = ($results | Measure-Object -Average).Average
Write-Host "Mean: $mean seconds"
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u pritunnel -n 50

# Verify port availability
sudo netstat -tlnp | grep 443

# Check permissions
sudo chown -R pritunnel:pritunnel /etc/pritunnel
sudo chmod 600 /etc/pritunnel/server.key
```

### Client Can't Connect

```bash
# Test server connectivity
telnet 192.168.1.33 443

# Check firewall
sudo ufw status
sudo iptables -L -n

# Verify certificate
openssl x509 -in /etc/pritunnel/server.crt -text -noout
```

### No Internet Through VPN

```bash
# Check IP forwarding
cat /proc/sys/net/ipv4/ip_forward  # Should be 1

# Check NAT rules
sudo iptables -t nat -L -n -v

# Verify routing
ip route show
```

### Slow Performance

```bash
# Check CPU usage
top -p $(pgrep pritunnel)

# Check network interface
ethtool eth0

# Increase thread pool in config
# thread_pool_size = 8

# Restart service
sudo systemctl restart pritunnel
```

---

## Performance Metrics

| Metric | Value |
|---|---|
| Mean Transfer Time | 0.305s |
| Overhead vs Baseline | 6.3% |
| Throughput | 571 KB/s |
| Setup Time | 9 minutes |
| Max Clients | 100+ |
| CPU Usage | Low |
| Memory Usage | 50 MB |

---

## Security Checklist

- [ ] TLS 1.3 enabled
- [ ] AES-256 cipher configured
- [ ] SHA256 authentication enabled
- [ ] Firewall rules configured
- [ ] IP forwarding enabled
- [ ] NAT rules configured
- [ ] Certificates generated
- [ ] Admin password changed
- [ ] Audit logging enabled
- [ ] 2FA configured
- [ ] User groups created
- [ ] Bandwidth limits set

---

## Default Ports

| Service | Port | Protocol |
|---|---|---|
| VPN Server | 443 | TCP/UDP |
| Management Console | 8000 | TCP |
| Alternative VPN | 8443 | TCP/UDP |
| HTTP Server | 8080 | TCP |

---

## File Locations

| File | Location |
|---|---|
| Config | `/etc/pritunnel/pritunnel.conf` |
| Server Key | `/etc/pritunnel/server.key` |
| Server Cert | `/etc/pritunnel/server.crt` |
| CA Cert | `/etc/pritunnel/ca.crt` |
| User Database | `/var/lib/pritunnel/users.db` |
| Log File | `/var/log/pritunnel/pritunnel.log` |
| Audit Log | `/var/log/pritunnel/audit.log` |

---

## User Management

### Create User (Web Console)

1. Click **Users** → **Add User**
2. Enter email, name, group
3. Click **Save**
4. Click **Generate Password**
5. Send credentials to user

### User Groups

- **Standard Users** - Basic VPN access
- **Administrators** - Full access
- **Power Users** - Elevated access

### Permissions

- VPN Access: Enable/Disable
- Server Access: Select servers
- Bandwidth Limit: Set limit (Mbps)
- Session Timeout: Set timeout (hours)

---

## Integration with GNS3

### Add to Topology

1. Right-click Ubuntu VM
2. Select **Console**
3. Run installation commands
4. Configure server
5. Test connectivity

### Router Configuration

```
interface Tunnel1
 ip address 10.8.0.254 255.255.255.0
 tunnel source 192.168.1.1
 tunnel destination 192.168.1.33
 tunnel mode gre
!
ip route 10.8.0.0 255.255.255.0 10.8.0.1
```

### Wireshark Capture

```
Filter: ip.addr == 10.8.0.0/24
```

---

## Performance Comparison

| VPN | Setup | Overhead | Best For |
|---|---|---|---|
| PriTunnel | 9 min | 6.3% | SMEs |
| GRE | 10 min | 6.5% | Tunneling |
| WireGuard | 15 min | 104.5% | Performance |
| OpenVPN | 20 min | 174.6% | Compatibility |
| IPSec | 20 min | 227.6% | Security |

---

## Useful Links

- **Documentation:** https://pritunnel.com/docs/
- **GitHub:** https://github.com/pritunnel/pritunnel
- **Downloads:** https://pritunnel.com/download/
- **Community:** https://pritunnel.com/community/

---

**Version:** 1.0  
**Last Updated:** 2025-01-15  
**Status:** Complete
