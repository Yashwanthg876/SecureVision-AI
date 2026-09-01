@echo off
echo Starting SecureVision AI Backend...
cd /d "%~dp0backend"
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
) else if exist "..\.venv\Scripts\python.exe" (
    ..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
) else (
    python -m uvicorn main:app --reload --port 8000
)
pause
