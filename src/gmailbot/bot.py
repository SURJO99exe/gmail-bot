import time
import random
import string
import pyautogui
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class GmailBot:
    def __init__(self):
        edge_options = Options()
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Edge(options=edge_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def _generate_random_string(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def type_human(self, text):
        """Simulate human typing using pyautogui."""
        for char in text:
            pyautogui.write(char)
            time.sleep(random.uniform(0.1, 0.3))

    def start_signup(self):
        """Navigate to the Google account creation page and fill form using direct keyboard simulation."""
        self.driver.get("https://accounts.google.com/signup")
        time.sleep(5) # Wait for page load
        
        # Random data
        first_name = "John"
        last_name = "Doe"
        username = f"jd{self._generate_random_string(10)}"
        password = f"Pass{self._generate_random_string(12)}!"

        try:
            # Step 1: Name
            # Just start typing, the first name field is usually auto-focused
            self.type_human(first_name)
            time.sleep(0.5)
            pyautogui.press('tab')
            time.sleep(0.5)
            self.type_human(last_name)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(5)
            
            # Step 2: Birthday & Gender
            self.type_human("15") # Day
            pyautogui.press('tab')
            time.sleep(0.5)
            self.type_human("January") # Month (type the name, it usually works for dropdowns)
            pyautogui.press('tab')
            time.sleep(0.5)
            self.type_human("1995") # Year
            pyautogui.press('tab')
            time.sleep(0.5)
            self.type_human("Male") # Gender
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(5)
            
            # Step 3: Username
            self.type_human(username)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(5)
            
            # Step 4: Password
            self.type_human(password)
            time.sleep(0.5)
            pyautogui.press('tab')
            time.sleep(0.5)
            self.type_human(password)
            time.sleep(0.5)
            pyautogui.press('enter')

            print(f"Generated Credentials: {username}@gmail.com / {password}")
            print("Action required: Phone verification might appear now.")
            time.sleep(10)
            
        except Exception as e:
            print(f"Human-like automation failed: {e}")
            try:
                self.driver.save_screenshot("error_screenshot.png")
            except:
                pass

    def quit(self):
        if self.driver:
            self.driver.quit()
