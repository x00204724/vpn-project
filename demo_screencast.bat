@echo off
REM VPN Screencast One-Click Demo (Windows + WSL)
REM Run this ^^^ to start full demo for recording!

echo ==============================================
echo  VPN Project Screencast Demo - READY TO RECORD
echo ==============================================
echo.

REM Enter WSL Ubuntu (assumes Ubuntu distro installed)
python3 demo_runner_fixed.py && read -p 'Press enter to exit demo'"

echo.
echo ==============================================
echo  ✅ SCREENCAST COMPLETE! Files updated:
echo  - demo_log.json (logs)
echo  - perf_results.json (baseline vs VPN)
echo  - health_check.json (ping/latency)
echo ==============================================
