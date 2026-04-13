@echo off
echo Post-Reboot WSL GRE Tunnel Setup - Run as Administrator!
echo =========================================================
echo.

REM Ensure WSL full install
echo [+] Finalizing WSL...
wsl --install --no-distribution
wsl --list -v

REM Launch Ubuntu first time
echo [+] Launching Ubuntu (set username/password)...
wsl -d Ubuntu
echo (Exited Ubuntu? Continue...)

REM Run setup in WSL
echo [+] Setting up GRE in Ubuntu...
wsl -d Ubuntu bash -c "cd /mnt/c/Users/Lenovo/project && sudo python3 setup_gre_tunnel.py"

echo [+] Verify:
wsl -d Ubuntu ip tunnel show gre0
wsl -d Ubuntu ping -c 3 10.0.0.2

echo.
echo Tunnel UP! Test from Windows: ping 10.0.0.1
pause
