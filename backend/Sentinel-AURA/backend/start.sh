#!/bin/bash
# Startup script for Sentinel-AURA Backend

echo "🚀 Starting Sentinel-AURA Backend..."

# Check if MongoDB is running (optional)
# mongod --version > /dev/null 2>&1
# if [ $? -ne 0 ]; then
#     echo "⚠️  MongoDB not found. Please ensure MongoDB is installed and running."
# fi

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000