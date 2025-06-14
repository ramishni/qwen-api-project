#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Start the FastAPI server in the background.
# Logs will be sent to stdout/stderr.
echo "Starting FastAPI server in the background..."
uvicorn main:app --host 0.0.0.0 --port 80 &

# Wait for a few seconds to ensure the server is up and running.
# A more robust solution would use a health check loop.
echo "Waiting for server to start..."
sleep 8

# Run the Qwen-Agent application.
# This script will connect to the FastAPI server we just started.
echo "Running Qwen-Agent application..."
python agent_app.py
