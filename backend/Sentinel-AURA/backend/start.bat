@echo off
REM Startup script for Sentinel-AURA Backend (Windows)

echo 🚀 Starting Sentinel-AURA Backend...

REM Install dependencies
pip install -r requirements.txt

REM Run the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000