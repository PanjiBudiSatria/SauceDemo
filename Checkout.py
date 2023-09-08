import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class SauceDemoCheckoutTest(unittest.TestCase):
    def setUp(self):
        chrome_driver_path = ChromeDriverManager().install()
        service = Service(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def login(self, username, password):
        self.driver.get('https://www.saucedemo.com/')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'user-name')))
        username_input = self.driver.find_element(By.ID, 'user-name')
        password_input = self.driver.find_element(By.ID, 'password')
        login_button = self.driver.find_element(By.ID, 'login-button')
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

    def add_item_to_cart(self, item_name):
        item_locator = (By.XPATH, f"//div[@class='inventory_item_name' and text()='{item_name}']")
        add_to_cart_button = self.driver.find_element(By.XPATH, f"{item_locator}/ancestor::div[@class='inventory_item_label']//button")
        add_to_cart_button.click()

    def remove_item_from_cart(self, item_name):
        item_locator = (By.XPATH, f"//div[@class='inventory_item_name' and text()='{item_name}']")
        remove_from_cart_button = self.driver.find_element(By.XPATH, f"{item_locator}/ancestor::div[@class='inventory_item_label']//button")
        remove_from_cart_button.click()

    def proceed_to_checkout(self):
        cart_button = self.driver.find_element(By.CLASS_NAME, 'shopping_cart_badge')
        cart_button.click()
        checkout_button = self.driver.find_element(By.ID, 'checkout')
        checkout_button.click()

        # Simulate entering shipping information (dummy data)
        first_name_input = self.driver.find_element(By.ID, 'first-name')
        last_name_input = self.driver.find_element(By.ID, 'last-name')
        postal_code_input = self.driver.find_element(By.ID, 'postal-code')
        continue_button = self.driver.find_element(By.ID, 'continue')

        # Fill in shipping information
        first_name_input.send_keys('John')
        last_name_input.send_keys('Doe')
        postal_code_input.send_keys('12345')

        # Continue to the next step
        continue_button.click()


    def go_back_to_homepage(self):
        continue_shopping_button = self.driver.find_element(By.ID, 'continue-shopping')
        continue_shopping_button.click()

    def test_shopping_scenario(self):
        self.login('standard_user', 'secret_sauce')
        
        # Add three items to the cart
        self.add_item_to_cart('Sauce Labs Backpack')
        self.add_item_to_cart('Sauce Labs Bolt T-Shirt')
        self.add_item_to_cart('Sauce Labs Onesie')
        
        # Proceed to checkout
        self.proceed_to_checkout()
        
        # Go back to the homepage
        self.go_back_to_homepage()

if __name__ == "__main__":
    unittest.main()
