from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome WebDriver with a specified window size
driver = webdriver.Chrome()

try:
    # Navigate to the homepage
    driver.get("http://127.0.0.1:5000/index")
    driver.maximize_window()
    
    # Test: Check the page title
    try:
        assert "HabitNest" in driver.title
        print("Test 1 Passed: Homepage title is correct.")
    except AssertionError:
        print("Test 1 Failed: Homepage title is incorrect.")
    
    # Wait until the login link is clickable, then click it
    try:
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Login'))
        )
        login_link.click()
        print("Test 2 Passed: Login link clicked successfully.")
    except Exception as e:
        print(f"Test 2 Failed: Could not click login link. Error: {e}")
    
    # Wait for the login section to be displayed
    time.sleep(2)
    
    # Find the email and password input fields
    try:
        email_input = driver.find_element(By.NAME, 'email')
        password_input = driver.find_element(By.NAME, 'password')
        print("Test 3 Passed: Email and password input fields found.")
    except Exception as e:
        print(f"Test 3 Failed: Could not find email and/or password input fields. Error: {e}")
    
    # Enter the login credentials
    try:
        email_input.send_keys("testuser@example.com")
        password_input.send_keys("testpassword")
        print("Test 4 Passed: Entered login credentials.")
    except Exception as e:
        print(f"Test 4 Failed: Could not enter login credentials. Error: {e}")
    
    # Submit the login form
    try:
        login_form = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_form.click()
        print("Test 5 Passed: Login form submitted.")
    except Exception as e:
        print(f"Test 5 Failed: Could not submit login form. Error: {e}")
    
    # Wait for the dashboard to load
    time.sleep(5)
    
    # Test: Check the dashboard page title
    try:
        assert "Dashboard" in driver.title
        print("Test 6 Passed: Dashboard title is correct.")
    except AssertionError:
        print("Test 6 Failed: Dashboard title is incorrect.")
    
finally:
    # Close the browser
    driver.quit()
