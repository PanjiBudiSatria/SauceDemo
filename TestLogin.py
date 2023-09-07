import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class SauceDemoLoginTest(unittest.TestCase):
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

    def test_positive_login(self):
        self.login('standard_user', 'secret_sauce')
        WebDriverWait(self.driver, 10).until(EC.title_contains('Swag Labs'))
        products_title = self.driver.title
        self.assertEqual(products_title, 'Swag Labs', "Login was unsuccessful")

    def test_negative_login(self):
        self.login('invalid_user', 'invalid_password')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h3[@data-test="error"]')))
        error_message_element = self.driver.find_element(By.XPATH, '//h3[@data-test="error"]')
        self.assertIsNotNone(error_message_element, "Error message not displayed")

    def test_blank_username_login(self):
        self.login('', 'secret_sauce')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h3[@data-test="error"]')))
        error_message_element = self.driver.find_element(By.XPATH,'//h3[@data-test="error"]')
        self.assertEqual(error_message_element.text, "Epic sadface: Username is required")

    def test_blank_password_login(self):
        self.login('standard_user', '')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h3[@data-test="error"]')))
        error_message_element = self.driver.find_element(By.XPATH,'//h3[@data-test="error"]')
        self.assertEqual(error_message_element.text, "Epic sadface: Password is required")

if __name__ == '__main__':
    # Create a test loader
    loader = unittest.TestLoader()

    # Create a test suite and add test methods to it
    suite = unittest.TestSuite()
    suite.addTest(SauceDemoLoginTest('test_positive_login'))
    suite.addTest(SauceDemoLoginTest('test_negative_login'))
    suite.addTest(SauceDemoLoginTest('test_blank_username_login'))
    suite.addTest(SauceDemoLoginTest('test_blank_password_login'))

    # Create a test runner and run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)