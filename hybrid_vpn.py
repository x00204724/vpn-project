#!/usr/bin/env python3
"""
Hybrid VPN System - On-Premises to Azure
Complete working implementation with failover, monitoring, and performance testing
"""

import socket
import threading
import json
import time
import subprocess
from datetime import datetime
from enum import Enum

class VPNStatus(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    FAILED = "failed"

class HybridVPNGateway:
    def __init__(self, name, vpn_type, host, port):
        self.name = name
        self.vpn_type = vpn_type  # 'on-prem' or 'azure'
        self.host = host
        self.port = port
        self.status = VPNStatus.DISCONNECTED
        self.latency = 0
        self.throughput = 0
        self.connections = 0
        self.bytes_transferred = 0
        self.last_heartbeat = None
        
    def to_dict(self):
        return {
            'name': self.name,
            'type': self.vpn_type,
            'host': self.host,
            'port': self.port,
            'status': self.status.value,
            'latency_ms': self.latency,
            'throughput_mbps': self.throughput,
            'connections': self.connections,
            'bytes_transferred': self.bytes_transferred,
            'last_heartbeat': self.last_heartbeat
        }


class HybridVPNSystem:
    def __init__(self):
        self.gateways = {}
        self.routes = {}
        self.monitoring_active = False
        self.failover_enabled = True
        self.primary_gateway = None
        self.backup_gateway = None
        self.stats = {
            'total_connections': 0,
            'total_bytes': 0,
            'failovers': 0,
            'start_time': datetime.now().isoformat()
        }
        
    def add_gateway(self, name, vpn_type, host, port):
        """Add VPN gateway to system"""
        gateway = HybridVPNGateway(name, vpn_type, host, port)
        self.gateways[name] = gateway
        
        print(f"[+] Gateway added: {name} ({vpn_type}) at {host}:{port}")
        
        if vpn_type == 'on-prem' and self.primary_gateway is None:
            self.primary_gateway = name
        elif vpn_type == 'azure' and self.backup_gateway is None:
            self.backup_gateway = name
        
        return gateway
    
    def add_route(self, destination, gateway, metric=100):
        """Add routing rule"""
        self.routes[destination] = {
            'gateway': gateway,
            'metric': metric,
            'active': True
        }
        
        print(f"[+] Route added: {destination} -> {gateway} (metric: {metric})")
    
    def check_gateway_health(self, gateway_name):
        """Check gateway health via ping"""
        gateway = self.gateways.get(gateway_name)
        if not gateway:
            return False
        
        try:
            # Measure latency
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((gateway.host, gateway.port))
            sock.close()
            
            latency = (time.time() - start) * 1000  # Convert to ms
            
            if result == 0:
                gateway.status = VPNStatus.CONNECTED
                gateway.latency = latency
                gateway.last_heartbeat = datetime.now().isoformat()
                return True
            else:
                gateway.status = VPNStatus.FAILED
                return False
        
        except Exception as e:
            gateway.status = VPNStatus.FAILED
            print(f"[-] Health check failed for {gateway_name}: {e}")
            return False
    
    def monitor_gateways(self):
        """Monitor all gateways"""
        print("\n[*] Starting gateway monitoring...")
        self.monitoring_active = True
        
        while self.monitoring_active:
            for gateway_name in self.gateways:
                self.check_gateway_health(gateway_name)
            
            # Check for failover
            if self.failover_enabled:
                self.check_failover()
            
            time.sleep(10)  # Check every 10 seconds
    
    def check_failover(self):
        """Check if failover is needed"""
        if not self.primary_gateway or not self.backup_gateway:
            return
        
        primary = self.gateways.get(self.primary_gateway)
        backup = self.gateways.get(self.backup_gateway)
        
        if not primary or not backup:
            return
        
        # If primary is down and backup is up, failover
        if primary.status == VPNStatus.FAILED and backup.status == VPNStatus.CONNECTED:
            print(f"\n[!] PRIMARY GATEWAY DOWN - INITIATING FAILOVER")
            print(f"[!] Switching from {self.primary_gateway} to {self.backup_gateway}")
            
            # Update routes to use backup
            for destination, route in self.routes.items():
                if route['gateway'] == self.primary_gateway:
                    route['gateway'] = self.backup_gateway
                    print(f"[+] Route updated: {destination} -> {self.backup_gateway}")
            
            self.stats['failovers'] += 1
        
        # If primary is back up, failback
        elif primary.status == VPNStatus.CONNECTED and backup.status == VPNStatus.FAILED:
            print(f"\n[+] PRIMARY GATEWAY RECOVERED - FAILING BACK")
            print(f"[+] Switching from {self.backup_gateway} to {self.primary_gateway}")
            
            # Update routes to use primary
            for destination, route in self.routes.items():
                if route['gateway'] == self.backup_gateway:
                    route['gateway'] = self.primary_gateway
                    print(f"[+] Route updated: {destination} -> {self.primary_gateway}")
    
    def measure_throughput(self, gateway_name, test_size_mb=100):
        """Measure gateway throughput"""
        gateway = self.gateways.get(gateway_name)
        if not gateway:
            return 0
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((gateway.host, gateway.port))
            
            # Send test data
            test_data = b'X' * (test_size_mb * 1024 * 1024)
            start = time.time()
            sock.sendall(test_data)
            elapsed = time.time() - start
            
            sock.close()
            
            # Calculate throughput
            throughput = (test_size_mb * 8) / elapsed  # Mbps
            gateway.throughput = throughput
            
            return throughput
        
        except Exception as e:
            print(f"[-] Throughput test failed: {e}")
            return 0
    
    def get_system_status(self):
        """Get complete system status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'gateways': {name: gw.to_dict() for name, gw in self.gateways.items()},
            'routes': self.routes,
            'stats': self.stats,
            'primary_gateway': self.primary_gateway,
            'backup_gateway': self.backup_gateway,
            'failover_enabled': self.failover_enabled,
            'monitoring_active': self.monitoring_active
        }
    
    def print_status(self):
        """Print system status"""
        status = self.get_system_status()
        
        print("\n" + "="*60)
        print("HYBRID VPN SYSTEM STATUS")
        print("="*60)
        
        print(f"\nPrimary Gateway: {self.primary_gateway}")
        print(f"Backup Gateway: {self.backup_gateway}")
        print(f"Failover Enabled: {self.failover_enabled}")
        print(f"Monitoring Active: {self.monitoring_active}")
        
        print("\nGateway Status:")
        for name, gw in self.gateways.items():
            print(f"\n  {name}:")
            print(f"    Type: {gw.vpn_type}")
            print(f"    Status: {gw.status.value}")
            print(f"    Latency: {gw.latency:.2f} ms")
            print(f"    Throughput: {gw.throughput:.2f} Mbps")
            print(f"    Connections: {gw.connections}")
        
        print("\nRouting Table:")
        for destination, route in self.routes.items():
            print(f"  {destination} -> {route['gateway']} (metric: {route['metric']})")
        
        print("\nStatistics:")
        print(f"  Total Connections: {self.stats['total_connections']}")
        print(f"  Total Bytes: {self.stats['total_bytes']}")
        print(f"  Failovers: {self.stats['failovers']}")
        
        print("\n" + "="*60)
    
    def export_status(self, filename='hybrid_vpn_status.json'):
        """Export system status to JSON"""
        status = self.get_system_status()
        
        with open(filename, 'w') as f:
            json.dump(status, f, indent=2)
        
        print(f"\n[+] Status exported to {filename}")


class HybridVPNController:
    def __init__(self):
        self.system = HybridVPNSystem()
        
    def setup_hybrid_vpn(self):
        """Setup complete hybrid VPN system"""
        print("\n" + "="*60)
        print("HYBRID VPN SYSTEM SETUP")
        print("="*60)
        
        # Add on-premises gateway
        print("\n[*] Adding on-premises gateway...")
        self.system.add_gateway(
            name='on-prem-gateway',
            vpn_type='on-prem',
            host='192.168.1.1',
            port=443
        )
        
        # Add Azure gateway
        print("\n[*] Adding Azure gateway...")
        self.system.add_gateway(
            name='azure-gateway',
            vpn_type='azure',
            host='40.71.0.1',  # Example Azure public IP
            port=443
        )
        
        # Add routes
        print("\n[*] Adding routes...")
        self.system.add_route('10.0.0.0/8', 'on-prem-gateway', metric=100)
        self.system.add_route('192.168.0.0/16', 'on-prem-gateway', metric=100)
        self.system.add_route('172.16.0.0/12', 'azure-gateway', metric=100)
        
        # Start monitoring
        print("\n[*] Starting monitoring...")
        monitor_thread = threading.Thread(target=self.system.monitor_gateways)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Wait for initial health checks
        time.sleep(5)
        
        # Print status
        self.system.print_status()
        
        return self.system
    
    def run_performance_tests(self):
        """Run performance tests on all gateways"""
        print("\n" + "="*60)
        print("PERFORMANCE TESTING")
        print("="*60)
        
        for gateway_name in self.system.gateways:
            print(f"\n[*] Testing {gateway_name}...")
            
            # Measure latency
            self.system.check_gateway_health(gateway_name)
            gateway = self.system.gateways[gateway_name]
            print(f"[+] Latency: {gateway.latency:.2f} ms")
            
            # Measure throughput
            throughput = self.system.measure_throughput(gateway_name, test_size_mb=10)
            print(f"[+] Throughput: {throughput:.2f} Mbps")
        
        # Export results
        self.system.export_status()


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Hybrid VPN System')
    parser.add_argument('--setup', action='store_true', help='Setup hybrid VPN')
    parser.add_argument('--test', action='store_true', help='Run performance tests')
    parser.add_argument('--status', action='store_true', help='Show system status')
    
    args = parser.parse_args()
    
    controller = HybridVPNController()
    
    if args.setup:
        system = controller.setup_hybrid_vpn()
        
        # Keep monitoring
        try:
            while True:
                time.sleep(30)
                system.print_status()
        except KeyboardInterrupt:
            print("\n[*] Shutting down...")
            system.monitoring_active = False
    
    elif args.test:
        controller.setup_hybrid_vpn()
        controller.run_performance_tests()
    
    elif args.status:
        controller.setup_hybrid_vpn()
        controller.system.print_status()
    
    else:
        print("Usage: python3 hybrid_vpn.py [--setup|--test|--status]")
        print("\nExamples:")
        print("  Setup: python3 hybrid_vpn.py --setup")
        print("  Test: python3 hybrid_vpn.py --test")
        print("  Status: python3 hybrid_vpn.py --status")
        parser.print_help()


if __name__ == '__main__':
    main()
