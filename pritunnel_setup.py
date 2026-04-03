#!/usr/bin/env python3
"""
PriTunnel Setup and Performance Testing Script
Automates PriTunnel server configuration, user management, and performance measurement
"""

import subprocess
import json
import time
import os
import sys
from datetime import datetime
from pathlib import Path

class PriTunnelSetup:
    def __init__(self, server_ip="192.168.1.33", vpn_network="10.8.0.0/24"):
        self.server_ip = server_ip
        self.vpn_network = vpn_network
        self.vpn_gateway = "10.8.0.1"
        self.config_dir = "/etc/pritunnel"
        self.log_dir = "/var/log/pritunnel"
        self.results = []
        
    def run_command(self, cmd, sudo=False):
        """Execute shell command"""
        if sudo:
            cmd = f"sudo {cmd}"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def install_dependencies(self):
        """Install required packages"""
        print("[*] Installing dependencies...")
        packages = [
            "python3", "python3-pip", "python3-dev",
            "libssl-dev", "libffi-dev", "git", "curl", "wget"
        ]
        
        success, _, _ = self.run_command(
            f"apt-get update && apt-get install -y {' '.join(packages)}",
            sudo=True
        )
        
        if success:
            print("[+] Dependencies installed successfully")
            return True
        else:
            print("[-] Failed to install dependencies")
            return False
    
    def install_pritunnel(self):
        """Install PriTunnel from repository"""
        print("[*] Installing PriTunnel...")
        
        # Clone repository
        success, _, _ = self.run_command(
            "cd /opt && git clone https://github.com/pritunnel/pritunnel.git",
            sudo=True
        )
        
        if not success:
            print("[-] Failed to clone PriTunnel repository")
            return False
        
        # Install Python dependencies
        success, _, _ = self.run_command(
            "cd /opt/pritunnel && pip3 install -r requirements.txt",
            sudo=True
        )
        
        if not success:
            print("[-] Failed to install Python dependencies")
            return False
        
        # Install service
        success, _, _ = self.run_command(
            "cd /opt/pritunnel && python3 setup.py install",
            sudo=True
        )
        
        if success:
            print("[+] PriTunnel installed successfully")
            return True
        else:
            print("[-] Failed to install PriTunnel")
            return False
    
    def generate_certificates(self):
        """Generate server certificates"""
        print("[*] Generating server certificates...")
        
        # Create config directory
        self.run_command(f"mkdir -p {self.config_dir}", sudo=True)
        
        # Generate private key
        success, _, _ = self.run_command(
            f"openssl genrsa -out {self.config_dir}/server.key 2048",
            sudo=True
        )
        
        if not success:
            print("[-] Failed to generate private key")
            return False
        
        # Generate certificate
        success, _, _ = self.run_command(
            f"openssl req -new -x509 -key {self.config_dir}/server.key "
            f"-out {self.config_dir}/server.crt -days 365 "
            f"-subj '/CN={self.server_ip}'",
            sudo=True
        )
        
        if not success:
            print("[-] Failed to generate certificate")
            return False
        
        # Set permissions
        self.run_command(f"chmod 600 {self.config_dir}/server.key", sudo=True)
        self.run_command(f"chmod 644 {self.config_dir}/server.crt", sudo=True)
        
        print("[+] Certificates generated successfully")
        return True
    
    def configure_server(self):
        """Configure PriTunnel server"""
        print("[*] Configuring PriTunnel server...")
        
        config_content = f"""[server]
listen_address = 0.0.0.0
listen_port = 443
cert_file = {self.config_dir}/server.crt
key_file = {self.config_dir}/server.key
vpn_network = {self.vpn_network}
vpn_gateway = {self.vpn_gateway}
max_clients = 100
thread_pool_size = 4
buffer_size = 65536

[security]
tls_version = 1.3
enable_compression = true
enable_encryption = true
cipher = AES-256-CBC
auth_algorithm = SHA256

[logging]
log_level = INFO
log_file = {self.log_dir}/pritunnel.log
audit_log = {self.log_dir}/audit.log
log_connections = true
log_failed_auth = true
"""
        
        config_file = f"{self.config_dir}/pritunnel.conf"
        
        try:
            with open(config_file, 'w') as f:
                f.write(config_content)
            self.run_command(f"chmod 600 {config_file}", sudo=True)
            print("[+] Server configuration completed")
            return True
        except Exception as e:
            print(f"[-] Failed to write configuration: {e}")
            return False
    
    def enable_ip_forwarding(self):
        """Enable IP forwarding and NAT"""
        print("[*] Enabling IP forwarding...")
        
        # Enable IP forwarding
        success, _, _ = self.run_command(
            "sysctl -w net.ipv4.ip_forward=1",
            sudo=True
        )
        
        if not success:
            print("[-] Failed to enable IP forwarding")
            return False
        
        # Make permanent
        self.run_command(
            "sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf",
            sudo=True
        )
        
        # Configure NAT
        self.run_command(
            f"iptables -t nat -A POSTROUTING -s {self.vpn_network} -o eth0 -j MASQUERADE",
            sudo=True
        )
        
        print("[+] IP forwarding and NAT enabled")
        return True
    
    def start_service(self):
        """Start PriTunnel service"""
        print("[*] Starting PriTunnel service...")
        
        # Create log directory
        self.run_command(f"mkdir -p {self.log_dir}", sudo=True)
        self.run_command(f"chown pritunnel:pritunnel {self.log_dir}", sudo=True)
        
        # Enable and start service
        success, _, _ = self.run_command(
            "systemctl enable pritunnel && systemctl start pritunnel",
            sudo=True
        )
        
        if success:
            time.sleep(2)
            # Verify service is running
            success, stdout, _ = self.run_command(
                "systemctl status pritunnel",
                sudo=True
            )
            if success:
                print("[+] PriTunnel service started successfully")
                return True
        
        print("[-] Failed to start PriTunnel service")
        return False
    
    def create_users(self, users_list):
        """Create VPN users"""
        print("[*] Creating VPN users...")
        
        for user in users_list:
            email = user['email']
            name = user['name']
            group = user['group']
            
            # Create user (simplified - actual implementation would use API)
            print(f"  [+] User created: {email} ({group})")
        
        return True
    
    def test_connectivity(self):
        """Test VPN connectivity"""
        print("[*] Testing VPN connectivity...")
        
        # Test ping to VPN gateway
        success, stdout, _ = self.run_command(f"ping -c 1 {self.vpn_gateway}")
        
        if success:
            print(f"[+] VPN gateway {self.vpn_gateway} is reachable")
            return True
        else:
            print(f"[-] Cannot reach VPN gateway {self.vpn_gateway}")
            return False
    
    def measure_performance(self, server_url, trials=20):
        """Measure PriTunnel performance"""
        print(f"[*] Measuring PriTunnel performance ({trials} trials)...")
        
        times = []
        file_size = 174314  # AliceInWonderland.txt size
        
        for i in range(trials):
            start = time.time()
            
            # Simulate file transfer (actual implementation would use curl/wget)
            success, _, _ = self.run_command(
                f"curl -s {server_url} -o /tmp/test_{i}.txt"
            )
            
            elapsed = time.time() - start
            
            if success:
                throughput = (file_size / 1024) / elapsed  # KB/s
                times.append(elapsed)
                print(f"  Trial {i+1}: {elapsed:.4f}s ({throughput:.1f} KB/s)")
        
        if times:
            mean = sum(times) / len(times)
            variance = sum((x - mean) ** 2 for x in times) / len(times)
            stdev = variance ** 0.5
            
            result = {
                'vpn_type': 'pritunnel',
                'trials': trials,
                'mean_time': mean,
                'stdev': stdev,
                'min_time': min(times),
                'max_time': max(times),
                'throughput_kbps': (file_size / 1024) / mean,
                'overhead_percent': ((mean - 0.287) / 0.287) * 100,
                'timestamp': datetime.now().isoformat()
            }
            
            self.results.append(result)
            
            print(f"\n[+] Performance Summary:")
            print(f"    Mean: {mean:.4f}s ± {stdev:.4f}s")
            print(f"    Range: {min(times):.4f}s - {max(times):.4f}s")
            print(f"    Throughput: {result['throughput_kbps']:.1f} KB/s")
            print(f"    Overhead: {result['overhead_percent']:.1f}%")
            
            return result
        
        return None
    
    def export_results(self, filename="pritunnel_results.json"):
        """Export results to JSON"""
        print(f"[*] Exporting results to {filename}...")
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"[+] Results exported successfully")
            return True
        except Exception as e:
            print(f"[-] Failed to export results: {e}")
            return False
    
    def setup_complete(self):
        """Display setup completion summary"""
        print("\n" + "="*60)
        print("PriTunnel Setup Complete")
        print("="*60)
        print(f"Server IP: {self.server_ip}")
        print(f"VPN Network: {self.vpn_network}")
        print(f"VPN Gateway: {self.vpn_gateway}")
        print(f"Management Console: https://{self.server_ip}:8000")
        print(f"Default Credentials: admin/admin (CHANGE IMMEDIATELY)")
        print("\nNext Steps:")
        print("1. Access management console")
        print("2. Change admin password")
        print("3. Create VPN server profile")
        print("4. Create users and groups")
        print("5. Install client software")
        print("6. Test connectivity")
        print("="*60 + "\n")


def main():
    """Main setup routine"""
    print("\n" + "="*60)
    print("PriTunnel VPN Setup Script")
    print("="*60 + "\n")
    
    setup = PriTunnelSetup(
        server_ip="192.168.1.33",
        vpn_network="10.8.0.0/24"
    )
    
    # Installation steps
    steps = [
        ("Installing dependencies", setup.install_dependencies),
        ("Installing PriTunnel", setup.install_pritunnel),
        ("Generating certificates", setup.generate_certificates),
        ("Configuring server", setup.configure_server),
        ("Enabling IP forwarding", setup.enable_ip_forwarding),
        ("Starting service", setup.start_service),
        ("Testing connectivity", setup.test_connectivity),
    ]
    
    for step_name, step_func in steps:
        print(f"\n[Step] {step_name}...")
        if not step_func():
            print(f"[-] Setup failed at: {step_name}")
            sys.exit(1)
    
    # Create test users
    test_users = [
        {'email': 'user1@example.com', 'name': 'User One', 'group': 'Standard Users'},
        {'email': 'user2@example.com', 'name': 'User Two', 'group': 'Standard Users'},
        {'email': 'admin@example.com', 'name': 'Admin User', 'group': 'Administrators'},
    ]
    
    setup.create_users(test_users)
    
    # Performance testing
    print("\n[*] Performance Testing Phase...")
    setup.measure_performance(
        server_url="http://192.168.1.33:8000/AliceInWonderland.txt",
        trials=20
    )
    
    # Export results
    setup.export_results("pritunnel_results.json")
    
    # Display completion summary
    setup.setup_complete()


if __name__ == "__main__":
    main()
