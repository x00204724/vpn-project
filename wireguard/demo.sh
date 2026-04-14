#!/bin/bash
# WireGuard Demo Script - Final Year Project
# Run in WSL Ubuntu after setup

echo "====================================="
echo "WireGuard VPN Demo Starting..."
echo "====================================="

# Bring up tunnel
sudo wg-quick up wg0

echo "
1. Interface Status:"
ip addr show wg0

echo "
2. WireGuard Status:"
wg show

echo "
3. Ping Test (10.0.0.2):"
ping -c 4 10.0.0.2

echo "
====================================="
echo "Demo Complete! Bringing down..."
echo "====================================="

sudo wg-quick down wg0

echo "Tunnel down. Ready for next demo run!"
