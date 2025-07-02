#!/usr/bin/env pwsh
# Clean up legacy v1 log monitoring app files and prepare repo for v2 modular structure

# 1. Remove old v1 scripts and tests
Remove-Item -Path ../log_monitor.py -ErrorAction SilentlyContinue
Remove-Item -Path ../test_log_monitor.py -ErrorAction SilentlyContinue

# 2. Remove old test logs (if any)
Remove-Item -Path ../test_logs.log -ErrorAction SilentlyContinue
Remove-Item -Path ../empty.log -ErrorAction SilentlyContinue

# 3. Remove any old documentation referencing v1
Remove-Item -Path ../OLD_README.md -ErrorAction SilentlyContinue
Remove-Item -Path ../OLD_USER_GUIDE.md -ErrorAction SilentlyContinue

# 4. Clean up .pyc and __pycache__
Get-ChildItem -Path .. -Include *.pyc -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path .. -Include __pycache__ -Recurse | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 5. (Optional) Tag last v1 commit in git before running this script
# git tag v1.2.0

Write-Host "Legacy v1 files cleaned up. Repo is now ready for v2+ modular structure."
