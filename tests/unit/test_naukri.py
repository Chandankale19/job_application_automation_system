import pytest
import logging
from unittest.mock import patch, MagicMock
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.automation.naukri import NaukriAutomation, NaukriError

@pytest.fixture
def mock_driver():
    """Create a mock WebDriver."""
    return MagicMock()

@pytest.fixture
def config():
    """Sample configuration."""
    return {
        'NAUKRI_USERNAME': 'test@example.com',
        'NAUKRI_PASSWORD': 'password',
        'KEYWORDS': 'software engineer',
        'LOCATION': 'Bangalore',
        'MAX_APPLICATIONS': 2
    }

@pytest.fixture(autouse=True)
def setup_logging():
    """Set up logging for tests."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_login_success(mock_driver, config):
    """Test successful login."""
    with patch('src.automation.naukri.WebDriverWait') as mock_wait:
        mock_wait.return_value.until.return_value = True
        naukri = NaukriAutomation(mock_driver, config)
        
        naukri.login()
        
        mock_driver.get.assert_called_with("https://www.naukri.com/nlogin/login")
        mock_driver.find_element.assert_any_call(By.ID, "usernameField")
        mock_driver.find_element.assert_any_call(By.ID, "passwordField")
        mock_driver.find_element.assert_any_call(By.XPATH, "//button[@type='submit']")
        logging.info("test_login_success passed")

def test_login_timeout(mock_driver, config):
    """Test login failure due to timeout."""
    with patch('src.automation.naukri.WebDriverWait') as mock_wait:
        mock_wait.return_value.until.side_effect = TimeoutException("Timeout")
        naukri = NaukriAutomation(mock_driver, config)
        
        with pytest.raises(NaukriError) as exc_info:
            naukri.login()
        assert "Login failed" in str(exc_info.value)
        logging.info("test_login_timeout passed")

def test_apply_to_jobs_success(mock_driver, config):
    """Test successful job applications."""
    with patch('src.automation.naukri.WebDriverWait') as mock_wait, \
         patch('src.automation.naukri.random_delay') as mock_delay:
        mock_wait.return_value.until.return_value = True
        mock_job = MagicMock()
        mock_job.find_element.return_value.is_enabled.return_value = True
        mock_driver.find_elements.return_value = [mock_job]
        
        naukri = NaukriAutomation(mock_driver, config)
        applications = naukri.apply_to_jobs()
        
        assert applications == 1
        mock_driver.get.assert_called_with("https://www.naukri.com/software-engineer-jobs-in-bangalore")
        mock_job.find_element.assert_called_with(By.XPATH, ".//button[contains(text(), 'Apply')]")
        logging.info("test_apply_to_jobs_success passed")

def test_apply_to_jobs_no_jobs(mock_driver, config):
    """Test job application with no jobs found."""
    with patch('src.automation.naukri.WebDriverWait') as mock_wait:
        mock_wait.return_value.until.return_value = True
        mock_driver.find_elements.return_value = []
        
        naukri = NaukriAutomation(mock_driver, config)
        applications = naukri.apply_to_jobs()
        
        assert applications == 0
        logging.info("test_apply_to_jobs_no_jobs passed")

def test_apply_to_jobs_invalid_config(mock_driver):
    """Test job application with invalid configuration."""
    config = {'KEYWORDS': '', 'LOCATION': '', 'MAX_APPLICATIONS': 2}
    naukri = NaukriAutomation(mock_driver, config)
    
    with pytest.raises(NaukriError) as exc_info:
        naukri.apply_to_jobs()
    assert "Keywords and location cannot be empty" in str(exc_info.value)
    logging.info("test_apply_to_jobs_invalid_config passed")
