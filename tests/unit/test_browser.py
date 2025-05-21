import pytest
import logging
from unittest.mock import patch, MagicMock
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from src.automation.browser import setup_browser, BrowserError

@pytest.fixture(autouse=True)
def setup_logging():
    """Set up logging for tests."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_setup_browser_success():
    """Test successful browser setup and cleanup."""
    with patch('src.automation.browser.webdriver.Chrome') as mock_chrome:
        mock_driver = MagicMock(spec=WebDriver)
        mock_chrome.return_value = mock_driver
        
        with setup_browser() as driver:
            assert driver == mock_driver
            mock_driver.set_page_load_timeout.assert_called_with(30)
        
        mock_driver.quit.assert_called_once()
        logging.info("test_setup_browser_success passed")

def test_setup_browser_failure():
    """Test browser setup failure handling."""
    with patch('src.automation.browser.webdriver.Chrome', side_effect=WebDriverException("Driver error")):
        with pytest.raises(BrowserError) as exc_info:
            with setup_browser():
                pass
        assert "Browser setup failed" in str(exc_info.value)
        logging.info("test_setup_browser_failure passed")

def test_browser_cleanup_on_exception():
    """Test browser cleanup when an exception occurs."""
    with patch('src.automation.browser.webdriver.Chrome') as mock_chrome:
        mock_driver = MagicMock(spec=WebDriver)
        mock_chrome.return_value = mock_driver
        
        with pytest.raises(RuntimeError):
            with setup_browser() as driver:
                raise RuntimeError("Test error")
        
        mock_driver.quit.assert_called_once()
        logging.info("test_browser_cleanup_on_exception passed")
