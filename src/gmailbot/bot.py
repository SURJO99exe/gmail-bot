from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class GmailBot:
    def __init__(self):
        chrome_options = Options()
        # Add options to make the bot look more human
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        # Change the property value to undefined to avoid detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def start_signup(self):
        """Navigate to the Google account creation page."""
        self.driver.get("https://accounts.google.com/signup")
        # The bot will wait for the page to load
        time.sleep(2)
        
    def quit(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
