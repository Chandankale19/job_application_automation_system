import logging
import signal
import sys
from scheduler.job_scheduler import start_scheduler
from config.settings import load_config
from logger.logging_config import setup_logging

def handle_shutdown(signum, frame):
    """Handle graceful shutdown on SIGINT or SIGTERM."""
    logging.info("Received shutdown signal, exiting gracefully...")
    sys.exit(0)

def main():
    """Main entry point for the Naukri Auto Apply system."""
    try:
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, handle_shutdown)
        signal.signal(signal.SIGTERM, handle_shutdown)
        
        setup_logging()
        load_config()
        logging.info("Starting Naukri Auto Apply system")
        start_scheduler()
    except Exception as e:
        logging.critical(f"Fatal error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
