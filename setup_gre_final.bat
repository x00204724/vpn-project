@echo off
echo GRE Tunnel Auto-Setup - Run as Administrator!
echo ==============================================
echo.

REM Check admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Run as Administrator!
    pause
    exit /b 1
)

echo [+] Admin confirmed.

REM Enable RRAS features (standard names for Windows 10/11)
echo [+] Enabling RRAS features...
dism /online /enable-feature /all /FeatureName:RasRoutingProtocols-IP /quiet /norestart
dism /online /enable-feature /all /FeatureName:RasRip /quiet /norestart
dism /online /enable-feature /all /FeatureName:RemoteAccess /quiet /norestart
dism /online /enable-feature /all /FeatureName:RemoteAccess-AdvancedSecurity /quiet /norestart

echo [+] RRAS enabled (reboot if prompted).

REM Run Python setup
echo [+] Running Python GRE setup...
python setup_gre_tunnel.py

echo [+] Verifying...
netsh interface ipv4 show interface | findstr gre
route print | findstr 10.0.0
ping 10.0.0.2 -n 4

echo.
echo Done! Check above for status.
pause
