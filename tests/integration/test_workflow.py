import pytest
import logging
from unittest.mock import patch, MagicMock
from src.scheduler.job_scheduler import job_application_task
from src.config.settings import load_config

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
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_workflow_success(config):
    """Test end-to-end workflow (mocked)."""
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
        logging.info("test_workflow_success passed")
