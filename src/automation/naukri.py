from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import logging
from .utils import random_delay, retry
from typing import Dict

class NaukriError(Exception):
    """Custom exception for Naukri automation errors."""
    pass

class NaukriAutomation:
    """Handles automation tasks for Naukri.com."""
    
    def __init__(self, driver, config: Dict[str, any]):
        self.driver = driver
        self.config = config
        self.base_url = "https://www.naukri.com"
    
    @retry(attempts=3, delay=5)
    def login(self):
        """Log in to Naukri.com with retries."""
        try:
            self.driver.get(f"{self.base_url}/nlogin/login")
            WebDriverWait(self.driver, 10).until(EC.title_contains("Naukri"))
            logging.info("Naukri login page loaded")
            
            username_field = self.driver.find_element(By.ID, "usernameField")
            password_field = self.driver.find_element(By.ID, "passwordField")
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            
            username_field.send_keys(self.config['NAUKRI_USERNAME'])
            random_delay(1, 3)
            password_field.send_keys(self.config['NAUKRI_PASSWORD'])
            random_delay(1, 3)
            submit_button.click()
            
            WebDriverWait(self.driver, 15).until(EC.url_contains("my.naukri.com"))
            logging.info("Logged in successfully")
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Login failed: {str(e)}")
            raise NaukriError(f"Login failed: {str(e)}")
    
    def apply_to_jobs(self):
        """Search for jobs and apply to up to MAX_APPLICATIONS jobs."""
        try:
            # Construct and validate search URL
            keywords = self.config['KEYWORDS'].strip().replace(' ', '-')
            location = self.config['LOCATION'].strip().lower().replace(' ', '-')
            if not keywords or not location:
                logging.error("Invalid keywords or location")
                raise NaukriError("Keywords and location cannot be empty")
            
            search_url = f"{self.base_url}/{keywords}-jobs-in-{location}"
            self.driver.get(search_url)
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
            )
            logging.info("Job search page loaded")
            
            jobs = self.driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")
            if not jobs:
                logging.warning("No jobs found for the given search criteria")
                return 0
            
            application_count = 0
            for job in jobs[:self.config['MAX_APPLICATIONS']]:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", job)
                    random_delay(1, 3)
                    
                    apply_button = job.find_element(By.XPATH, ".//button[contains(text(), 'Apply')]")
                    if not apply_button.is_enabled():
                        logging.debug("Apply button disabled, skipping job")
                        continue
                    
                    apply_button.click()
                    random_delay(2, 5)
                    
                    # Check for questionnaire or popups
                    if self.driver.find_elements(By.CLASS_NAME, "questionnaire"):
                        logging.info("Questionnaire detected, skipping job")
                        continue
                    
                    application_count += 1
                    logging.info(f"Applied to job {application_count}")
                    
                    if application_count >= self.config['MAX_APPLICATIONS']:
                        logging.info("Reached daily application limit")
                        break
                except (NoSuchElementException, ElementClickInterceptedException) as e:
                    logging.warning(f"Failed to apply to a job: {str(e)}")
                    continue
                except Exception as e:
                    logging.error(f"Unexpected error applying to job: {str(e)}")
                    continue
            
            logging.info(f"Successfully applied to {application_count} jobs")
            return application_count
        except TimeoutException as e:
            logging.error(f"Timeout during job application: {str(e)}")
            raise NaukriError(f"Job application timeout: {str(e)}")
        except Exception as e:
            logging.error(f"Error during job application: {str(e)}")
            raise NaukriError(f"Job application failed: {str(e)}")
