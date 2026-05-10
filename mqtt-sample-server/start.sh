#!/bin/bash

# MQTT Server Linux Startup Script
set -e

echo "========================================"
echo "   MQTT Server Starter (Linux)"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Step 1: Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created."
else
    echo "[1/4] Virtual environment already exists."
fi

# Step 2: Activate virtual environment
echo "[2/4] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated."

# Step 3: Install dependencies
echo "[3/4] Installing dependencies..."
pip install -q -U pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed."

# Step 4: Start MQTT Server in background
echo ""
echo "[4/4] Starting MQTT Server in background..."
echo "========================================"

# Start server in background with logging
nohup python mqtt_server.py > mqtt-server.log 2>&1 < /dev/null &
echo $! > mqtt-server.pid

echo ""
echo "✓ MQTT Server started!"
echo "  PID: $(cat mqtt-server.pid)"
echo "  Log file: $SCRIPT_DIR/mqtt-server.log"
echo ""
echo "To stop the server:"
echo "  kill $(cat mqtt-server.pid)"
echo "  or"
echo "  ./start-daemon.sh stop"
