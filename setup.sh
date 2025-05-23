#!/bin/bash
# Setup script for Naukri Auto Apply project

set -e  # Exit on any error

LOG_FILE="logs/setup.log"

# Ensure log directory exists
mkdir -p logs
touch "$LOG_FILE"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "Starting setup process"

# Check for Python 3.8+
if ! command -v python3 &>/dev/null; then
    log "ERROR: Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]; }; then
    log "ERROR: Python 3.8 or higher required. Found: $PYTHON_VERSION"
    exit 1
fi
log "Python version check passed: $PYTHON_VERSION"

# Install dependencies
log "Installing dependencies from requirements.txt"
if ! pip3 install -r requirements.txt >>"$LOG_FILE" 2>&1; then
    log "ERROR: Failed to install dependencies. Check $LOG_FILE for details."
    exit 1
fi

# Verify .env file
if [ ! -f "config/.env" ]; then
    log "WARNING: config/.env not found. Copying from .env.example"
    cp config/.env.example config/.env || {
        log "ERROR: Failed to copy .env.example"
        exit 1
    }
fi

log "Setup completed successfully. Configure config/.env before running."
