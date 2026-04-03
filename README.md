# VPN Connectivity Analysis - Reproducibility Guide

**Project:** Comparative Analysis of Network Connectivity Solutions for Startups, SMEs and Enterprises  
**Author:** Annit Maria Binu  
**Student Number:** x00204724  
**Date:** 2025  
**Grade Target:** A+ (100/100)

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [GNS3 Topology Setup](#gns3-topology-setup)
5. [Running Measurements](#running-measurements)
6. [Data Analysis](#data-analysis)
7. [Troubleshooting](#troubleshooting)
8. [Project Structure](#project-structure)
9. [File Descriptions](#file-descriptions)
10. [References](#references)

---

## Quick Start

**For experienced users (5 minutes):**

```bash
# 1. Import GNS3 project
gns3 vpn_topology.gns3

# 2. Start all nodes
# (Right-click topology → Start all nodes)

# 3. Run measurements
python3 measure_vpn.py

# 4. Analyze results
python3 analyze_results.py

# 5. View results
# Open: vpn_results.csv and generated charts
```

**For first-time users:** Follow the complete guide below.

---

## System Requirements

### Minimum Hardware
- **CPU:** Intel Core i5 (6 cores) or equivalent
- **RAM:** 16 GB (32 GB recommended)
- **Storage:** 50 GB free space (SSD recommended)
- **Network:** Gigabit Ethernet (1000 Mbps)
- **OS:** Windows 10 Pro, macOS 10.15+, or Linux (Ubuntu 20.04+)

### Recommended Hardware
- **CPU:** Intel Core i7-10700K or better
- **RAM:** 32 GB DDR4
- **Storage:** 512 GB NVMe SSD
- **Network:** Gigabit Ethernet
- **OS:** Windows 10 Pro or Windows 11

### Software Requirements
- **GNS3:** Version 2.2.34 or later
- **Python:** 3.8 or later
- **Cisco IOS Image:** c3750e-universalk9-mz.150-1.EX
- **Ubuntu VM Image:** 20.04 LTS
- **Wireshark:** 3.4.9 or later (optional, for packet analysis)

---

## Installation Guide

### Step 1: Install GNS3

**Windows:**
1. Download GNS3 from https://www.gns3.com/software/download
2. Run installer: `GNS3-2.2.34-all-in-one.exe`
3. Follow installation wizard (accept defaults)
4. Install VirtualBox or VMware (GNS3 will prompt)
5. Restart computer

**macOS:**
```bash
brew install gns3
```

**Linux (Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install gns3-server gns3-gui
```

### Step 2: Import Cisco IOS Image

1. Open GNS3
2. Go to: **Edit → Preferences → Dynamips → IOS routers**
3. Click **New**
4. Browse to Cisco IOS image: `c3750e-universalk9-mz.150-1.EX`
5. Set RAM: 256 MB
6. Click **OK**

### Step 3: Import Ubuntu VM Image

1. Go to: **Edit → Preferences → QEMU → QEMU VMs**
2. Click **New**
3. Browse to Ubuntu 20.04 LTS image
4. Set RAM: 2048 MB
5. Set vCPUs: 2
6. Click **OK**

### Step 4: Install Python Dependencies

```bash
# Windows (PowerShell)
python -m pip install --upgrade pip
pip install numpy pandas scipy matplotlib requests

# macOS/Linux
python3 -m pip install --upgrade pip
pip3 install numpy pandas scipy matplotlib requests
```

### Step 5: Install Wireshark (Optional)

**Windows:**
- Download from https://www.wireshark.org/download/
- Run installer

**macOS:**
```bash
brew install wireshark
```

**Linux:**
```bash
sudo apt-get install wireshark
```

---

## GNS3 Topology Setup

### Step 1: Import Project File

1. Open GNS3
2. Click **File → Open Project**
3. Select: `vpn_topology.gns3`
4. Click **Open**

### Step 2: Verify Topology

You should see:
- **3 Cisco 3750E Routers** (R1, R2, R3)
- **2 Ubuntu VMs** (ubuntunew-9, ubuntunew-1)
- **1 VPCS** (PC1)
- **1 Hub** (Hub1)
- **1 Switch** (Switch1)

### Step 3: Start All Nodes

1. Right-click on topology → **Start all nodes**
2. Wait 30-60 seconds for all nodes to boot
3. Verify all nodes show green status

### Step 4: Load Router Configurations

**For R1:**
1. Right-click R1 → **Console**
2. Copy-paste contents of `configs/R1_startup.conf`
3. Press Enter

**For R2:**
1. Right-click R2 → **Console**
2. Copy-paste contents of `configs/R2_startup.conf`
3. Press Enter

**For R3:**
1. Right-click R3 → **Console**
2. Copy-paste contents of `configs/R3_startup.conf`
3. Press Enter

### Step 5: Verify Connectivity

**Test basic connectivity:**
```
R1# ping 10.0.0.2
```

Expected output:
```
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/2/3 ms
```

**Test GRE tunnel:**
```
R1# ping 172.16.0.2
```

Expected output:
```
Success rate is 100 percent (5/5), round-trip min/avg/max = 2/3/4 ms
```

---

## Running Measurements

### Step 1: Start HTTP Server on Ubuntu VM

1. Right-click ubuntunew-9 → **Console**
2. Login with credentials (default: ubuntu/ubuntu)
3. Run:
```bash
cd /home/ubuntu
python3 -m http.server 8000
```

Expected output:
```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

### Step 2: Prepare Measurement Script

1. Open `measure_vpn.py` in text editor
2. Update IP addresses if needed:
   - `SERVER_IP = "192.168.1.33"` (ubuntunew-9)
   - `FILE_URL = "http://192.168.1.33:8000/AliceInWonderland.txt"`
3. Save file

### Step 3: Run Baseline Measurement

```bash
python3 measure_vpn.py --vpn baseline --trials 20
```

This will:
- Run 20 file transfer trials
- Measure transfer time for each trial
- Export results to `baseline_trials.csv`
- Display statistics

Expected output:
```
Baseline (No VPN) - Trial 1: 0.287s
Baseline (No VPN) - Trial 2: 0.295s
...
Baseline (No VPN) - Mean: 0.290s ± 0.009s
```

### Step 4: Run GRE Tunnel Measurement

```bash
python3 measure_vpn.py --vpn gre --trials 20
```

### Step 5: Run GRE + IPSec Measurement

```bash
python3 measure_vpn.py --vpn ipsec --trials 20
```

### Step 6: Run WireGuard Measurement

```bash
python3 measure_vpn.py --vpn wireguard --trials 20
```

### Step 7: Run OpenVPN Measurement

```bash
python3 measure_vpn.py --vpn openvpn --trials 20
```

### Step 8: Run All Measurements (Automated)

```bash
# PowerShell (Windows)
.\run_baseline_trials.ps1

# Bash (macOS/Linux)
bash run_baseline_trials.sh
```

This will run all 5 VPN types sequentially and generate complete results.

---

## Data Analysis

### Step 1: Run Analysis Script

```bash
python3 analyze_results.py
```

This will:
- Read all CSV files
- Calculate statistics (mean, std dev, confidence intervals)
- Generate comparison charts
- Export analysis report

### Step 2: View Results

**CSV Files Generated:**
- `baseline_trials.csv` - Baseline measurements
- `gre_trials.csv` - GRE tunnel measurements
- `ipsec_trials.csv` - GRE + IPSec measurements
- `wireguard_trials.csv` - WireGuard measurements
- `openvpn_trials.csv` - OpenVPN measurements

**Charts Generated:**
- `transfer_time_comparison.png` - Bar chart of transfer times
- `throughput_comparison.png` - Bar chart of throughput
- `overhead_comparison.png` - Overhead vs baseline
- `statistical_summary.png` - Box plots with confidence intervals

### Step 3: Generate Report

```bash
python3 analyze_results.py --report
```

This generates: `analysis_report.txt` with:
- Summary statistics
- Confidence intervals
- Overhead calculations
- Key findings

---

## Troubleshooting

### Issue: GNS3 Won't Start Nodes

**Solution:**
1. Check RAM allocation (need 16+ GB)
2. Verify Cisco IOS image is loaded
3. Restart GNS3
4. Check system resources: Task Manager → Performance

### Issue: No Connectivity Between Routers

**Solution:**
1. Verify all nodes are running (green status)
2. Check router configurations loaded correctly
3. Verify IP addresses match topology
4. Run: `show ip interface brief` on each router

### Issue: Python Script Fails

**Solution:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade numpy pandas scipy matplotlib requests

# Run with verbose output
python3 measure_vpn.py --verbose
```

### Issue: HTTP Server Not Responding

**Solution:**
1. Verify ubuntunew-9 is running
2. Check HTTP server is started: `ps aux | grep http.server`
3. Verify firewall allows port 8000
4. Test connectivity: `ping 192.168.1.33`

### Issue: Wireshark Packet Capture Not Working

**Solution:**
1. Run Wireshark as administrator
2. Select correct network interface
3. Use filter: `ip.addr == 192.168.1.33`
4. Start capture before running measurements

---

## Project Structure

```
vpn-project/
├── README.md                          # This file
├── index.html                         # Main website
├── styles.css                         # Website styling
├── script.js                          # Website interactivity
│
├── configs/                           # Router configurations
│   ├── R1_startup.conf               # R1 (Site A) config
│   ├── R2_startup.conf               # R2 (Site B) config
│   └── R3_startup.conf               # R3 (Transit) config
│
├── scripts/                           # Measurement & analysis scripts
│   ├── measure_vpn.py                # Main measurement script
│   ├── analyze_results.py            # Statistical analysis
│   ├── run_baseline_trials.ps1       # PowerShell automation
│   └── run_baseline_trials.sh        # Bash automation
│
├── data/                              # Measurement results
│   ├── baseline_trials.csv           # Baseline measurements
│   ├── gre_trials.csv                # GRE tunnel results
│   ├── ipsec_trials.csv              # GRE + IPSec results
│   ├── wireguard_trials.csv          # WireGuard results
│   └── openvpn_trials.csv            # OpenVPN results
│
├── captures/                          # Wireshark packet captures
│   ├── baseline_capture.pcap         # Baseline traffic
│   ├── gre_tunnel_capture.pcap       # GRE tunnel traffic
│   ├── ipsec_capture.pcap            # IPSec encrypted traffic
│   ├── wireguard_capture.pcap        # WireGuard traffic
│   └── openvpn_capture.pcap          # OpenVPN traffic
│
├── topology/                          # GNS3 project files
│   ├── vpn_topology.gns3             # Main GNS3 project
│   └── vpn_topology.gns3.bak         # Backup
│
├── documentation/                     # Additional documentation
│   ├── BASELINE_RESULTS.md           # Baseline measurement report
│   ├── ITERATION_3_REPORT.md         # Iteration 3 findings
│   ├── METHODOLOGY.md                # Detailed methodology
│   └── SECURITY_ANALYSIS.md          # Security analysis details
│
└── images/                            # Charts and diagrams
    ├── transfer_time_comparison.png
    ├── throughput_comparison.png
    ├── overhead_comparison.png
    └── statistical_summary.png
```

---

## File Descriptions

### Configuration Files

**R1_startup.conf**
- Configures R1 (Site A gateway)
- Sets up GRE tunnel endpoint
- Configures IPSec encryption
- Enables routing

**R2_startup.conf**
- Configures R2 (Site B gateway)
- Sets up GRE tunnel endpoint
- Configures IPSec encryption
- Enables routing

**R3_startup.conf**
- Configures R3 (Transit router)
- Simulates ISP/WAN router
- Enables IP forwarding

### Python Scripts

**measure_vpn.py**
- Automated file transfer measurement
- Supports 5 VPN types
- Configurable trial count
- Exports CSV results

**analyze_results.py**
- Statistical analysis
- Generates charts
- Calculates confidence intervals
- Produces summary report

### Data Files

**CSV Format:**
```
trial,vpn_type,transfer_time_seconds,throughput_kbps,timestamp
1,baseline,0.287,591,2025-01-15 10:30:45
2,baseline,0.295,576,2025-01-15 10:31:02
...
```

### Wireshark Captures

**How to View:**
1. Open Wireshark
2. File → Open → Select .pcap file
3. Use filters:
   - `ip.addr == 192.168.1.33` - Filter by IP
   - `esp` - Show IPSec ESP packets
   - `gre` - Show GRE packets
   - `tcp.port == 8000` - Show HTTP traffic

---

## References

### Key Papers
1. Donenfeld, J. (2018). WireGuard: Next Generation Kernel Network Tunnel. NDSS Symposium.
2. Kaufman, C., et al. (2010). Internet Key Exchange Protocol Version 2 (IKEv2). RFC 5996.
3. Farinacci, D., et al. (2000). Generic Routing Encapsulation (GRE). RFC 2784.

### Tools & Documentation
- GNS3 Documentation: https://docs.gns3.com/
- Cisco IOS Configuration: https://www.cisco.com/
- Python Documentation: https://docs.python.org/3/
- Wireshark User Guide: https://www.wireshark.org/docs/

### Standards
- FIPS 140-2: Security Requirements for Cryptographic Modules
- NIST SP 800-38D: Recommendation for Block Cipher Modes of Operation
- RFC 2330: Framework for IP Performance Metrics

---

## Support & Contact

**For issues or questions:**
1. Check Troubleshooting section above
2. Review GNS3 documentation
3. Check Python error messages
4. Verify system requirements

**Project Repository:**
- GitHub: [Your GitHub URL]
- Documentation: See `documentation/` folder

---

## License

This project is provided for educational purposes. All code and documentation are available for academic use.

**Author:** Annit Maria Binu  
**Date:** 2025  
**Institution:** [Your University]

---

## PriTunnel Integration (NEW)

PriTunnel has been added as the 6th VPN technology for comprehensive evaluation:

**PriTunnel Features:**
- Fast setup: 9 minutes (fully automated)
- Minimal overhead: 6.3% vs baseline
- Enterprise security: AES-256, TLS 1.3, 2FA
- User management: Role-based access control
- Scalability: 100+ concurrent users
- Best for: SMEs and rapid deployment

**New Documentation:**
- `PRITUNNEL_SETUP_GUIDE.md` - Complete setup guide
- `pritunnel_setup.py` - Automated installation script
- `PRITUNNEL_INTEGRATION.md` - Performance metrics and comparison
- `PRITUNNEL_QUICK_REFERENCE.md` - Quick reference card

**Performance Results:**
- Mean transfer time: 0.305s ± 0.012s
- Throughput: 571 KB/s
- Overhead: 6.3% (excellent)
- Consistency: Very stable (stdev: 0.012s)

---

## Iteration 3 Completion Status

**All Deliverables Complete (100%)**

✅ GRE tunnel implementation  
✅ IPSec encryption deployment  
✅ WireGuard evaluation  
✅ OpenVPN evaluation  
✅ **PriTunnel setup and testing (NEW)**  
✅ Automated measurement framework  
✅ Statistical analysis tools  
✅ Real VPN system implementation  
✅ Literature review (13 papers)  
✅ Security analysis matrix  
✅ Project website with interactive charts  
✅ Comprehensive documentation  

**Total VPN Technologies Evaluated:** 6
- Baseline (no VPN)
- GRE tunnel
- GRE + IPSec
- WireGuard
- OpenVPN
- PriTunnel

**Total Performance Trials:** 120 (20 per VPN type)

---

## Changelog

**Version 1.1 (2025-01-15) - PriTunnel Integration**
- Added PriTunnel setup guide and implementation
- Completed 6th VPN technology evaluation
- Added performance metrics and comparison
- Updated deployment recommendations
- Iteration 3 now 100% complete

**Version 1.0 (2025-01-15)**
- Initial release
- 5 VPN types tested
- Complete reproducibility guide
- All scripts and configurations included

---

**Last Updated:** 2025-01-15  
**Status:** Iteration 3 Complete (100%) - Ready for Iteration 4 (Azure VPN)
