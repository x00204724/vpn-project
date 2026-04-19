@echo off
echo ==============================================
echo VPN SCREENCast - STEP BY STEP DEMO
echo ==============================================
timeout /t 2 /nobreak >nul

echo STEP 1: Files
dir vpn_tools
timeout /t 3 /nobreak >nul

echo STEP 2: Measurements Data
type vpn_measurements.json
timeout /t 5 /nobreak >nul

echo STEP 3: Local Baseline Transfer
cd vpn_tools
python -m http.server 8000
timeout /t 2 /nobreak >nul

start http://localhost:8000

echo STEP 4: Dashboard
python dashboard.py
timeout /t 3 /nobreak >nul

echo STEP 5: HTML Demos
start ..\website\vpn-live-demo.html
start ..\website\index.html

echo STEP 6: Results
dir *.json *.csv
type vpn_measurements.json

echo ==============================================
echo END SCREENCast - Win+G stop!
pause

