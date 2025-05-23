#!/bin/bash
# Run script for Naukri Auto Apply project

set -e  # Exit on any error

LOG_FILE="logs/run.log"

# Ensure log directory exists
mkdir -p logs
touch "$LOG_FILE"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "Starting application"

# Check for Python 3
if ! command -v python3 &>/dev/null; then
    log "ERROR: Python 3 not found. Run ./scripts/setup.sh first."
    exit 1
fi

# Check for .env file
if [ ! -f "config/.env" ]; then
    log "ERROR: config/.env not found. Configure it based on config/.env.example."
    exit 1
fi

# Run the application
log "Executing src/main.py"
if ! python3 src/main.py >>"$LOG_FILE" 2>&1; then
    log "ERROR: Application failed. Check $LOG_FILE for details."
    exit 1
fi

log "Application running successfully"
