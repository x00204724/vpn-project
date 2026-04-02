# Data Transparency Statement

## VPN Connectivity Analysis Project - Data Sources

**Author:** Annit Maria Binu  
**Student Number:** x00204724  
**Date:** 2025-01-15

---

## Real vs Simulated Data Breakdown

### ✅ **REAL MEASURED DATA**

**Baseline Performance (No VPN):**
- **Source:** Actual HTTP server file transfer testing
- **Method:** Python HTTP server on localhost (192.168.1.33:8000)
- **File:** AliceInWonderland.txt (170 KB)
- **Trials:** 20 complete trials with timestamps
- **Results:** Mean 8.08s ± 9.68s, Range: 0.45s - 32.21s
- **Evidence:** baseline_trials.csv with raw data
- **Validation:** All transfers completed successfully

### ⚠️ **SIMULATED/ESTIMATED DATA**

**VPN Performance Measurements:**
- **GRE Tunnel:** Estimated +6.2% overhead (based on 24-byte header)
- **GRE + IPSec:** Estimated +227% overhead (based on encryption studies)
- **WireGuard:** Estimated +104% overhead (based on literature)
- **OpenVPN:** Estimated +174% overhead (based on benchmarks)

**Data Sources for Estimates:**
1. **Literature Review:** Academic papers on VPN performance
2. **Theoretical Analysis:** Known encryption overhead percentages
3. **Industry Benchmarks:** Published WireGuard vs OpenVPN comparisons
4. **Applied to Real Baseline:** Percentage increases applied to actual 8.08s baseline

### 📋 **DOCUMENTED BUT NOT IMPLEMENTED**

**GNS3 Topology:**
- **Status:** Designed and documented
- **Files:** Router configuration files exist
- **Reality:** Not fully tested with actual tunnels
- **Evidence:** Configuration files in repository

**Wireshark Captures:**
- **Status:** Planned and documented
- **Reality:** No actual .pcap files generated
- **Evidence:** Methodology documented

**Azure Hybrid VPN:**
- **Status:** Architecture designed
- **Reality:** Not implemented
- **Evidence:** Documentation only

---

## Academic Honesty Statement

This project demonstrates:

1. **Real baseline performance measurement** using proper statistical methods
2. **Comprehensive research** into VPN technologies and security
3. **Theoretical analysis** of encryption overhead based on literature
4. **Professional documentation** of planned implementations
5. **Honest disclosure** of what's real vs simulated

**Limitation:** Complete VPN tunnel implementation requires additional time and resources. This project provides the framework and baseline data for future completion.

**Academic Value:** The combination of real baseline data, theoretical analysis, and comprehensive documentation provides educational value and demonstrates understanding of VPN technologies.

---

## Data Files in Repository

### Real Data Files:
- `baseline_trials.csv` - 20 actual file transfer measurements
- `measure_vpn.py` - Python script used for measurements
- `analyze_results.py` - Statistical analysis tools

### Simulated Data Files:
- Performance estimates in website tables
- Charts showing theoretical comparisons
- Security analysis based on literature

### Documentation Files:
- Router configuration files (R1, R2, R3)
- GNS3 topology documentation
- Methodology and reproducibility guides

---

## Recommendations for Future Work

1. **Complete GNS3 Implementation:** Build working tunnels and measure real VPN performance
2. **Generate Wireshark Captures:** Actual packet analysis of encrypted traffic
3. **Azure Integration:** Implement hybrid cloud VPN with real measurements
4. **Larger File Testing:** Test with various file sizes to validate overhead calculations
5. **Hardware Testing:** Move from simulation to real router hardware

---

**Conclusion:** This project provides honest, transparent analysis with clear distinction between real measurements and theoretical estimates. The baseline data is genuine, and the VPN estimates are based on solid academic research.