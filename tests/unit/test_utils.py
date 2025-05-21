import pytest
import logging
import time
from unittest.mock import patch
from src.automation.utils import random_delay, retry

@pytest.fixture(autouse=True)
def setup_logging():
    """Set up logging for tests."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_random_delay():
    """Test random delay within bounds."""
    with patch('src.automation.utils.time.sleep') as mock_sleep:
        random_delay(1, 3)
        delay = mock_sleep.call_args[0][0]
        assert 1 <= delay <= 3
        logging.info("test_random_delay passed")

def test_retry_success():
    """Test retry decorator on successful function."""
    @retry(attempts=3, delay=1)
    def success_func():
        return "Success"
    
    with patch('src.automation.utils.random_delay') as mock_delay:
        result = success_func()
        assert result == "Success"
        mock_delay.assert_not_called()
        logging.info("test_retry_success passed")

def test_retry_failure():
    """Test retry decorator on failing function."""
    @retry(attempts=2, delay=1)
    def fail_func():
        raise ValueError("Test error")
    
    with patch('src.automation.utils.random_delay') as mock_delay:
        with pytest.raises(ValueError) as exc_info:
            fail_func()
        assert "Test error" in str(exc_info.value)
        assert mock_delay.call_count == 1
        logging.info("test_retry_failure passed")
