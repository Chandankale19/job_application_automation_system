import pytest
import logging
from unittest.mock import patch, MagicMock
from src.scheduler.job_scheduler import job_application_task, start_scheduler, SchedulerError
from src.config.settings import ConfigError

@pytest.fixture
def config():
    """Sample configuration."""
    return {
        'NAUKRI_USERNAME': 'test@example.com',
        'NAUKRI_PASSWORD': 'password',
        'KEYWORDS': 'software engineer',
        'LOCATION': 'Bangalore',
        'SCHEDULE_TIME': '09:00',
        'MAX_APPLICATIONS': 2
    }

@pytest.fixture(autouse=True)
def setup_logging():
    """Set up logging for tests."""
    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.info("Logging configured for test_scheduler")
    except Exception as e:
        print(f"Failed to configure logging: {str(e)}")
        raise

def test_job_application_task_success(config):
    """Test successful job application task."""
    try:
        with patch('src.scheduler.job_scheduler.load_config', return_value=config), \
             patch('src.scheduler.job_scheduler.setup_browser') as mock_browser, \
             patch('src.scheduler.job_scheduler.NaukriAutomation') as mock_naukri:
            mock_driver = MagicMock()
            mock_browser().__enter__.return_value = mock_driver
            mock_naukri.return_value.apply_to_jobs.return_value = 2
            
            job_application_task()
            
            mock_naukri.return_value.login.assert_called_once()
            mock_naukri.return_value.apply_to_jobs.assert_called_once()
            mock_browser().__exit__.assert_called_once()
            logging.info("test_job_application_task_success passed")
    except Exception as e:
        logging.error(f"Test test_job_application_task_success failed: {str(e)}")
        raise

def test_job_application_task_config_error():
    """Test job application task with config error."""
    try:
        with patch('src.scheduler.job_scheduler.load_config', side_effect=ConfigError("Config error")):
            job_application_task()  # Should not raise, logs error
            logging.info("test_job_application_task_config_error passed")
    except Exception as e:
        logging.error(f"Test test_job_application_task_config_error failed: {str(e)}")
        raise

def test_start_scheduler_success(config):
    """Test scheduler startup."""
    try:
        with patch('src.scheduler.job_scheduler.load_config', return_value=config), \
             patch('src.scheduler.job_scheduler.schedule.every') as mock_schedule, \
             patch('src.scheduler.job_scheduler.time.sleep') as mock_sleep:
            mock_schedule.return_value.day.at.return_value.do.return_value = None
            
            try:
                start_scheduler()
            except KeyboardInterrupt:
                pass
            
            mock_schedule.return_value.day.at.assert_called_with('09:00')
            logging.info("test_start_scheduler_success passed")
    except Exception as e:
        logging.error(f"Test test_start_scheduler_success failed: {str(e)}")
        raise

def test_start_scheduler_config_error():
    """Test scheduler failure due to config error."""
    try:
        with patch('src.scheduler.job_scheduler.load_config', side_effect=ConfigError("Config error")):
            with pytest.raises(SchedulerError) as exc_info:
                start_scheduler()
            assert "Config error" in str(exc_info.value)
            logging.info("test_start_scheduler_config_error passed")
    except Exception as e:
        logging.error(f"Test test_start_scheduler_config_error failed: {str(e)}")
        raise
