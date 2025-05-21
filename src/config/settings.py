import os
from dotenv import load_dotenv
import logging
from typing import Dict

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

def load_config() -> Dict[str, any]:
    """Load and validate configuration from .env file."""
    try:
        load_dotenv()
        
        config = {
            'NAUKRI_USERNAME': os.getenv('NAUKRI_USERNAME'),
            'NAUKRI_PASSWORD': os.getenv('NAUKRI_PASSWORD'),
            'KEYWORDS': os.getenv('KEYWORDS', 'software engineer'),
            'LOCATION': os.getenv('LOCATION', 'Bangalore'),
            'SCHEDULE_TIME': os.getenv('SCHEDULE_TIME', '09:00'),
            'MAX_APPLICATIONS': os.getenv('MAX_APPLICATIONS', '50')
        }
        
        # Validate required fields
        required_fields = ['NAUKRI_USERNAME', 'NAUKRI_PASSWORD']
        for field in required_fields:
            if not config[field]:
                logging.error(f"Missing required environment variable: {field}")
                raise ConfigError(f"Missing required environment variable: {field}")
        
        # Validate SCHEDULE_TIME format (HH:MM)
        try:
            hour, minute = map(int, config['SCHEDULE_TIME'].split(':'))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
        except ValueError:
            logging.error(f"Invalid SCHEDULE_TIME format: {config['SCHEDULE_TIME']}. Expected HH:MM")
            raise ConfigError(f"Invalid SCHEDULE_TIME format: {config['SCHEDULE_TIME']}")
        
        # Validate MAX_APPLICATIONS
        try:
            config['MAX_APPLICATIONS'] = int(config['MAX_APPLICATIONS'])
            if config['MAX_APPLICATIONS'] <= 0 or config['MAX_APPLICATIONS'] > 50:
                logging.error(f"MAX_APPLICATIONS must be between 1 and 50: {config['MAX_APPLICATIONS']}")
                raise ConfigError("MAX_APPLICATIONS must be between 1 and 50")
        except ValueError:
            logging.error(f"Invalid MAX_APPLICATIONS: {config['MAX_APPLICATIONS']}. Must be an integer")
            raise ConfigError("MAX_APPLICATIONS must be an integer")
        
        logging.info("Configuration loaded successfully")
        return config
    except Exception as e:
        logging.critical(f"Failed to load configuration: {str(e)}")
        raise ConfigError(f"Configuration loading failed: {str(e)}")
