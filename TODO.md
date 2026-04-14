# VPN Project TODO

## Completed ✅
- WireGuard setup + automation tools (vpn_tools/)
- Python VPN system (vpn_system.py, 14.51x overhead measured)
- GRE tunnel scripts
- Pritunl setup scripts/docs
- Azure/hybrid VPN scripts
- Dashboards (vpn_dashboard.py)
- Performance measurements (GNS3 + Python)

## Pending ⏳
1. Deploy Azure VPN: `python azure_vpn.py --deploy` (requires az login)
2. Run Pritunl: `python pritunnel_setup.py`
3. Multi-machine WireGuard (beyond loopback)
4. GNS3 integration for Pritunl/Azure
5. Update website with new perf charts
6. Full reproducibility test (run_baseline_trials.ps1)

## Testing Commands
- `cd vpn_tools && python auto_demo.py`
- `python vpn_system.py`
- `python vpn_dashboard.py`

