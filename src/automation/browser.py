from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
from contextlib import contextmanager
from selenium.common.exceptions import WebDriverException

class BrowserError(Exception):
    """Custom exception for browser-related errors."""
    pass

@contextmanager
def setup_browser():
    """Set up and yield a Selenium WebDriver instance, ensuring cleanup."""
    driver = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.set_page_load_timeout(30)
        logging.info("Browser setup completed successfully")
        yield driver
    except WebDriverException as e:
        logging.error(f"Failed to set up browser: {str(e)}")
        raise BrowserError(f"Browser setup failed: {str(e)}")
    finally:
        if driver:
            try:
                driver.quit()
                logging.info("Browser closed successfully")
            except Exception as e:
                logging.warning(f"Error closing browser: {str(e)}")
