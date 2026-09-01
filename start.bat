@echo off
echo Launching SecureVision AI Backend and Frontend...
start "SecureVision Backend" cmd /k "%~dp0run_backend.bat"
start "SecureVision Frontend" cmd /k "%~dp0run_frontend.bat"
echo Both services launched in separate windows!
