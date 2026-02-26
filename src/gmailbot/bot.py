import time
import random
import string
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
        
        self.driver = webdriver.Edge(options=edge_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def _generate_random_string(self, length=8):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def start_signup(self):
        """Navigate to the Google account creation page and fill initial form."""
        self.driver.get("https://accounts.google.com/signup")
        wait = WebDriverWait(self.driver, 30)
        
        # Random data
        first_name = "John"
        last_name = "Doe"
        username = f"jd{self._generate_random_string(10)}"
        password = f"Pass{self._generate_random_string(12)}!"

        def fill_field_js(element, value):
            try:
                self.driver.execute_script("arguments[0].focus();", element)
                self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
                self.driver.execute_script("arguments[0].blur();", element)
            except Exception as e:
                print(f"JS Fill failed: {e}")

        try:
            # --- Step 1: Name ---
            # Try finding by different locators for resilience
            first_name_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='firstName']")))
            fill_field_js(first_name_field, first_name)
            
            last_name_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='lastName']")
            fill_field_js(last_name_field, last_name)
            
            # Find Next button by text content inside button
            next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Next']/..|//button[contains(., 'Next')]")))
            self.driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)
            
            # --- Step 2: Birthday & Gender ---
            day_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='day']")))
            fill_field_js(day_field, "15")
            
            # Google often uses custom selects. We'll try to find the hidden select or use send_keys if visible.
            try:
                month_select = self.driver.find_element(By.ID, "month")
                month_select.send_keys("January")
            except:
                pass
            
            year_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='year']")
            fill_field_js(year_field, "1995")
            
            try:
                gender_select = self.driver.find_element(By.ID, "gender")
                gender_select.send_keys("Male")
            except:
                pass
            
            next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Next']/..|//button[contains(., 'Next')]")))
            self.driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)
            
            # --- Step 3: Choose Username ---
            # Wait for either Username field or suggestions
            username_container = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='Username']|//div[contains(text(), 'Create your own')]|//div[@id='selectionc1']")))
            
            create_own = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Create your own')]")
            if create_own:
                self.driver.execute_script("arguments[0].click();", create_own[0])
                time.sleep(2)

            username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='Username']")))
            fill_field_js(username_field, username)
            
            next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Next']/..|//button[contains(., 'Next')]")))
            self.driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)
            
            # --- Step 4: Password ---
            pass_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='Passwd']")))
            fill_field_js(pass_field, password)
            
            confirm_field = self.driver.find_element(By.CSS_SELECTOR, "input[name='ConfirmPasswd']")
            fill_field_js(confirm_field, password)
            
            next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button//span[text()='Next']/..|//button[contains(., 'Next')]")))
            self.driver.execute_script("arguments[0].click();", next_button)

            print(f"Generated Credentials: {username}@gmail.com / {password}")
            print("Action required: Phone verification might appear now.")
            time.sleep(10)
            
        except Exception as e:
            print(f"Automation failed: {str(e)[:200]}")
            # Take a screenshot for debugging if it fails
            try:
                self.driver.save_screenshot("error_screenshot.png")
                print("Screenshot saved as error_screenshot.png")
            except:
                pass
            
        except Exception as e:
            print(f"Automation step failed: {e}")

    def quit(self):
        if self.driver:
            self.driver.quit()
