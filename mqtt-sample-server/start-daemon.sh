#!/bin/bash

# MQTT Server Linux Daemon Startup Script
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Function to check virtual environment
setup_venv() {
    if [ ! -d "venv" ]; then
        log "Creating virtual environment..."
        python3 -m venv venv
        log "Virtual environment created."
    fi
    
    source venv/bin/activate
    
    log "Installing dependencies..."
    pip install -q -U pip
    pip install -q -r requirements.txt
    log "Dependencies installed."
}

# Function to start the server in background
start_server() {
    log "Starting MQTT Server..."
    
    setup_venv
    
    # Start server in background, log output
    nohup python mqtt_server.py > mqtt-server.log 2>&1 < /dev/null &
    echo $! > mqtt-server.pid
    
    log "MQTT Server started with PID: $(cat mqtt-server.pid)"
    log "Logs available at: $SCRIPT_DIR/mqtt-server.log"
}

# Function to stop the server
stop_server() {
    if [ -f "mqtt-server.pid" ]; then
        PID=$(cat mqtt-server.pid 2>/dev/null || true)
        if [ -n "$PID" ]; then
            log "Stopping MQTT Server (PID: $PID)..."
            kill "$PID" 2>/dev/null || true
            rm -f mqtt-server.pid
            log "MQTT Server stopped."
        else
            log_error "PID file exists but is empty."
        fi
    else
        log_error "No PID file found. Is the server running?"
    fi
}

# Function to check status
status_server() {
    if [ -f "mqtt-server.pid" ]; then
        PID=$(cat mqtt-server.pid 2>/dev/null || true)
        if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
            log "MQTT Server is running (PID: $PID)"
            exit 0
        fi
    fi
    log "MQTT Server is not running"
    exit 1
}

# Main script
case "${1:-start}" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        stop_server
        sleep 1
        start_server
        ;;
    status)
        status_server
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
