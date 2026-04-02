# Reproducibility Checklist

**Project:** VPN Connectivity Analysis  
**Author:** Annit Maria Binu  
**Date:** 2025

Use this checklist to verify that all components are in place for successful project reproduction.

---

## Pre-Reproduction Verification

### System Requirements
- [ ] Windows 10 Pro / macOS 10.15+ / Ubuntu 20.04+
- [ ] CPU: Intel Core i5 (6 cores) or equivalent
- [ ] RAM: 16 GB minimum (32 GB recommended)
- [ ] Storage: 50 GB free space
- [ ] Network: Gigabit Ethernet connection

### Software Installation
- [ ] GNS3 2.2.34 or later installed
- [ ] Python 3.8 or later installed
- [ ] Cisco IOS image (c3750e-universalk9-mz.150-1.EX) available
- [ ] Ubuntu 20.04 LTS VM image available
- [ ] Wireshark 3.4.9 or later (optional)

### Python Dependencies
- [ ] NumPy installed: `pip list | grep numpy`
- [ ] Pandas installed: `pip list | grep pandas`
- [ ] SciPy installed: `pip list | grep scipy`
- [ ] Matplotlib installed: `pip list | grep matplotlib`
- [ ] Requests installed: `pip list | grep requests`

---

## Project Files Verification

### Documentation Files
- [ ] README.md present and readable
- [ ] REPRODUCIBILITY_CHECKLIST.md (this file)
- [ ] METHODOLOGY.md with detailed procedures
- [ ] BASELINE_RESULTS.md with baseline data
- [ ] ITERATION_3_REPORT.md with findings

### Configuration Files
- [ ] configs/R1_startup.conf exists
- [ ] configs/R2_startup.conf exists
- [ ] configs/R3_startup.conf exists
- [ ] All configs are readable text files

### Python Scripts
- [ ] scripts/measure_vpn.py exists and is executable
- [ ] scripts/analyze_results.py exists and is executable
- [ ] scripts/run_baseline_trials.ps1 exists (Windows)
- [ ] scripts/run_baseline_trials.sh exists (macOS/Linux)

### GNS3 Project Files
- [ ] topology/vpn_topology.gns3 exists
- [ ] topology/vpn_topology.gns3.bak exists (backup)
- [ ] Project file is not corrupted

### Data Files
- [ ] data/baseline_trials.csv exists
- [ ] data/gre_trials.csv exists
- [ ] data/ipsec_trials.csv exists
- [ ] data/wireguard_trials.csv exists
- [ ] data/openvpn_trials.csv exists

### Wireshark Captures
- [ ] captures/baseline_capture.pcap exists
- [ ] captures/gre_tunnel_capture.pcap exists
- [ ] captures/ipsec_capture.pcap exists
- [ ] captures/wireguard_capture.pcap exists
- [ ] captures/openvpn_capture.pcap exists

### Website Files
- [ ] index.html exists and is valid HTML
- [ ] styles.css exists and is valid CSS
- [ ] script.js exists and is valid JavaScript
- [ ] Website opens in browser without errors

---

## GNS3 Setup Verification

### Cisco IOS Configuration
- [ ] Cisco IOS image imported in GNS3
- [ ] Image path verified: Edit → Preferences → Dynamips → IOS routers
- [ ] RAM set to 256 MB
- [ ] Image shows as "Ready"

### Ubuntu VM Configuration
- [ ] Ubuntu 20.04 LTS image imported in GNS3
- [ ] Image path verified: Edit → Preferences → QEMU → QEMU VMs
- [ ] RAM set to 2048 MB
- [ ] vCPUs set to 2
- [ ] Image shows as "Ready"

### Project Import
- [ ] vpn_topology.gns3 opens without errors
- [ ] All 7 nodes visible in topology
- [ ] Topology shows: R1, R2, R3, ubuntunew-9, ubuntunew-1, PC1, Hub1, Switch1

### Node Startup
- [ ] All nodes start successfully
- [ ] All nodes show green status after 60 seconds
- [ ] No error messages in GNS3 console
- [ ] CPU usage is reasonable (< 80%)

### Connectivity Verification
- [ ] R1 can ping R2: `ping 10.0.0.2` (success rate 100%)
- [ ] R1 can ping R3: `ping 10.0.0.3` (success rate 100%)
- [ ] GRE tunnel is up: `show interface tunnel0` (status: up)
- [ ] Tunnel can ping: `ping 172.16.0.2` (success rate 100%)

---

## Configuration Verification

### R1 Configuration
- [ ] Interface Fa0/1: 192.168.1.1/24 (up/up)
- [ ] Interface Fa0/0: 10.0.0.1/24 (up/up)
- [ ] Tunnel0: 172.16.0.1/24 (up/up)
- [ ] GRE tunnel configured correctly
- [ ] IPSec encryption enabled (if applicable)
- [ ] Routing table includes tunnel route

### R2 Configuration
- [ ] Interface Fa0/0: 10.0.0.2/24 (up/up)
- [ ] Interface Fa0/1: 192.168.2.1/24 (up/up)
- [ ] Tunnel0: 172.16.0.2/24 (up/up)
- [ ] GRE tunnel configured correctly
- [ ] IPSec encryption enabled (if applicable)
- [ ] Routing table includes tunnel route

### R3 Configuration
- [ ] Interface Fa0/0: 10.0.0.3/24 (up/up)
- [ ] Interface Fa0/1: 10.0.0.4/24 (up/up)
- [ ] IP forwarding enabled
- [ ] No tunnel configuration (transit router only)

### Ubuntu VM Configuration
- [ ] ubuntunew-9: IP 192.168.1.33 configured
- [ ] ubuntunew-1: IP 192.168.2.33 configured (or similar)
- [ ] Both VMs can ping their gateway
- [ ] Both VMs have internet connectivity (if needed)

---

## Measurement Verification

### Baseline Measurement
- [ ] HTTP server starts on ubuntunew-9: `python3 -m http.server 8000`
- [ ] Server responds to requests: `curl http://192.168.1.33:8000/`
- [ ] AliceInWonderland.txt file exists and is 170 KB
- [ ] File is accessible via HTTP
- [ ] Baseline measurement runs without errors
- [ ] 20 trials completed successfully
- [ ] Results exported to baseline_trials.csv
- [ ] Mean transfer time: ~0.290s ± 0.009s

### GRE Tunnel Measurement
- [ ] GRE tunnel is active and passing traffic
- [ ] Measurement runs without errors
- [ ] 20 trials completed successfully
- [ ] Results exported to gre_trials.csv
- [ ] Mean transfer time: ~0.308s ± 0.011s
- [ ] Overhead vs baseline: ~6.2%

### GRE + IPSec Measurement
- [ ] IPSec encryption is active
- [ ] Tunnel shows encrypted traffic in Wireshark
- [ ] Measurement runs without errors
- [ ] 20 trials completed successfully
- [ ] Results exported to ipsec_trials.csv
- [ ] Mean transfer time: ~0.948s ± 0.058s
- [ ] Overhead vs baseline: ~227%

### WireGuard Measurement
- [ ] WireGuard is installed and configured
- [ ] Tunnel is active and passing traffic
- [ ] Measurement runs without errors
- [ ] 20 trials completed successfully
- [ ] Results exported to wireguard_trials.csv
- [ ] Mean transfer time: ~0.592s ± 0.032s
- [ ] Overhead vs baseline: ~104%

### OpenVPN Measurement
- [ ] OpenVPN is installed and configured
- [ ] Tunnel is active and passing traffic
- [ ] Measurement runs without errors
- [ ] 20 trials completed successfully
- [ ] Results exported to openvpn_trials.csv
- [ ] Mean transfer time: ~0.795s ± 0.032s
- [ ] Overhead vs baseline: ~174%

---

## Data Analysis Verification

### Statistical Analysis
- [ ] analyze_results.py runs without errors
- [ ] All CSV files are read successfully
- [ ] Mean and standard deviation calculated correctly
- [ ] Confidence intervals computed (95% CI)
- [ ] Overhead percentages calculated
- [ ] Throughput values computed (KB/s)

### Chart Generation
- [ ] transfer_time_comparison.png generated
- [ ] throughput_comparison.png generated
- [ ] overhead_comparison.png generated
- [ ] statistical_summary.png generated
- [ ] All charts are readable and properly labeled
- [ ] Charts show expected trends

### Report Generation
- [ ] analysis_report.txt generated
- [ ] Report includes summary statistics
- [ ] Report includes confidence intervals
- [ ] Report includes key findings
- [ ] Report is readable and well-formatted

---

## Wireshark Verification

### Packet Capture Files
- [ ] baseline_capture.pcap opens in Wireshark
- [ ] gre_tunnel_capture.pcap opens in Wireshark
- [ ] ipsec_capture.pcap opens in Wireshark
- [ ] wireguard_capture.pcap opens in Wireshark
- [ ] openvpn_capture.pcap opens in Wireshark

### Baseline Traffic Analysis
- [ ] Packets show unencrypted HTTP traffic
- [ ] Source/destination IPs are correct
- [ ] Port 8000 (HTTP) is visible
- [ ] Payload is readable

### GRE Tunnel Analysis
- [ ] Packets show GRE encapsulation (protocol 47)
- [ ] Outer IP headers show tunnel endpoints
- [ ] Inner IP headers show original source/destination
- [ ] Payload is visible but encapsulated

### IPSec Traffic Analysis
- [ ] Packets show ESP headers (protocol 50)
- [ ] Payload is encrypted (appears as random data)
- [ ] No readable plaintext in payload
- [ ] Tunnel endpoints are correct

### WireGuard Traffic Analysis
- [ ] Packets show UDP port 51820 (default)
- [ ] Payload is encrypted
- [ ] No readable plaintext
- [ ] Tunnel is active

### OpenVPN Traffic Analysis
- [ ] Packets show UDP port 1194 (default)
- [ ] Payload is encrypted
- [ ] No readable plaintext
- [ ] Tunnel is active

---

## Website Verification

### HTML Structure
- [ ] index.html is valid HTML5
- [ ] All sections are present
- [ ] Navigation links work correctly
- [ ] No broken links

### CSS Styling
- [ ] styles.css loads without errors
- [ ] All elements are properly styled
- [ ] Colors are consistent
- [ ] Layout is responsive

### JavaScript Functionality
- [ ] script.js loads without errors
- [ ] File transfer animations work
- [ ] Charts render correctly
- [ ] Interactive elements respond to clicks
- [ ] No console errors

### Content Verification
- [ ] Overview section is complete
- [ ] Topology diagrams display correctly
- [ ] Methodology section is detailed
- [ ] Results section shows all data
- [ ] Security matrix is interactive
- [ ] Literature review is comprehensive
- [ ] Formal methodology is complete

---

## Final Verification

### Documentation Completeness
- [ ] All sections documented
- [ ] All procedures explained
- [ ] All files described
- [ ] All results reported
- [ ] All limitations noted

### Data Integrity
- [ ] All CSV files have correct format
- [ ] All data values are reasonable
- [ ] No missing values
- [ ] No corrupted files
- [ ] Checksums verified (if applicable)

### Reproducibility Confirmation
- [ ] Project can be set up from scratch
- [ ] All measurements can be re-run
- [ ] Results are consistent with documented values
- [ ] All procedures are documented
- [ ] All files are included

### Quality Assurance
- [ ] No errors in logs
- [ ] No warnings in GNS3
- [ ] No Python errors
- [ ] All tests pass
- [ ] All validations successful

---

## Sign-Off

**Reproducibility Verified By:** ___________________  
**Date:** ___________________  
**Status:** ☐ PASS ☐ FAIL

**Notes:**
```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________
```

---

**If all items are checked, the project is ready for reproduction and submission.**

For any failed items, refer to the Troubleshooting section in README.md.
