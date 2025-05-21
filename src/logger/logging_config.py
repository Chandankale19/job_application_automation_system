import logging
import logging.config
import yaml
import os
from typing import Dict

class LoggingConfigError(Exception):
    """Custom exception for logging configuration errors."""
    pass

def setup_logging():
    """Set up logging configuration from logging.yaml."""
    try:
        log_file = 'logs/naukri_auto_apply.log'
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        config_path = 'config/logging.yaml'
        if not os.path.exists(config_path):
            logging.warning(f"Logging config file not found: {config_path}. Using default config.")
            configure_default_logging(log_file)
            return
        
        with open(config_path, 'r') as f:
            config: Dict = yaml.safe_load(f)
        
        logging.config.dictConfig(config)
        logging.info("Logging configuration loaded successfully")
    except yaml.YAMLError as e:
        logging.error(f"Invalid YAML in logging config: {str(e)}")
        configure_default_logging(log_file)
    except Exception as e:
        logging.error(f"Failed to load logging config: {str(e)}")
        configure_default_logging(log_file)

def configure_default_logging(log_file: str):
    """Configure default logging if YAML config fails."""
    try:
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.info("Default logging configuration applied")
    except Exception as e:
        raise LoggingConfigError(f"Failed to configure default logging: {str(e)}")
