@echo off
echo ==============================================
echo VPN SCREENCast - FULL TERMINAL DEMO SEQUENCE
echo ==============================================
echo.

echo 1. Files:
cd vpn_tools
dir
cd ..

echo 2. Measurements:
type vpn_measurements.json

echo 3. Run VPN Auto Demo:
cd vpn_tools
python auto_demo.py --run

echo 4. Start Dashboard:
start python dashboard.py

echo 5. Open HTML Demos:
start website\index.html
start website\vpn-live-demo.html

echo 6. Results:
type perf_results.json
type demo_log.json
type health_check.json

echo ==============================================
echo RECORDING COMPLETE - Win+G stop
echo ==============================================
pause
