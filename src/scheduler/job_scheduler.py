import schedule
import time
import logging
from automation.naukri import NaukriAutomation, NaukriError
from automation.browser import setup_browser, BrowserError
from config.settings import load_config, ConfigError

class SchedulerError(Exception):
    """Custom exception for scheduler errors."""
    pass

def job_application_task():
    """Task to run the job application process."""
    logging.info("Starting job application task")
    try:
        config = load_config()
        with setup_browser() as driver:
            naukri = NaukriAutomation(driver, config)
            naukri.login()
            applications = naukri.apply_to_jobs()
            logging.info(f"Job application task completed with {applications} applications")
    except (ConfigError, BrowserError, NaukriError) as e:
        logging.error(f"Job application task failed: {str(e)}")
    except Exception as e:
        logging.critical(f"Unexpected error in job application task: {str(e)}")

def start_scheduler():
    """Start the scheduler to run the job application task daily."""
    try:
        config = load_config()
        schedule_time = config['SCHEDULE_TIME']
        
        schedule.every().day.at(schedule_time).do(job_application_task)
        logging.info(f"Scheduler started. Next run at {schedule_time} daily")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logging.info("Scheduler stopped by user")
                break
            except Exception as e:
                logging.error(f"Scheduler error: {str(e)}")
                time.sleep(60)  # Prevent tight loop on failure
    except ConfigError as e:
        logging.critical(f"Failed to start scheduler: {str(e)}")
        raise SchedulerError(str(e))
    except Exception as e:
        logging.critical(f"Unexpected error starting scheduler: {str(e)}")
        raise SchedulerError(f"Scheduler startup failed: {str(e)}")
