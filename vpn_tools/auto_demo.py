#!/usr/bin/env python3
    \"\"\"Automated VPN Demo Script
Full presentation demo sequence.\"\"\"
from wg_automation import WGAutomation
from vpn_health import VPNHealth
from perf_measure import PerfMeasure
from logger import Logger
import time
import sys

def run_full_demo():
    print('VPN DEMO STARTING...')
    print('='*50)
    
    log = Logger('demo_log.json')
    log.log('Demo started')
    
    # 1. WireGuard automation
    log.log('Starting WireGuard tunnel')
    wg = WGAutomation()
    
    if wg.up():
        time.sleep(3)  # Wait for handshake
        wg.handshake_status()
        
        # 2. Health check
        log.log('Running health check')
        health = VPNHealth()
        health.ping_test()
        health.print_report()
        
        # 3. Performance measurement
        log.log('Running performance test')
        perf = PerfMeasure()
        perf.measure_vpn()
        perf.compare()
        
        # 4. Status
        wg.status()
        
        wg.down()
        log.log('Demo complete')
    else:
        log.log('Tunnel failed to start', 'ERROR')
    
    log.summary()
    print('\\nDEMO COMPLETE! Check demo_log.json')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--run':
        run_full_demo()
    else:
        print('Usage: python auto_demo.py --run')

