from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome WebDriver with a specified window size
driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000/index")
driver.maximize_window()

try:
    # Test: Check the page title
    try:
        assert "HabitNest" in driver.title
        print("Test 1 Passed: Homepage title is correct.")
    except AssertionError:
        print("Test 1 Failed: Homepage title is incorrect.")

    # Wait until the login link is clickable, then click it
    try:
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'login-link'))
        )
        login_link.click()
        print("Test 2 Passed: Login link clicked successfully.")
    except Exception as e:
        print(f"Test 2 Failed: Could not click login link. Error: {e}")

    # Wait for the login page to load
    time.sleep(2)

    # Click the register link
    try:
        register_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Register Now'))
        )
        register_link.click()
        print("Test 3 Passed: Register link clicked successfully.")
    except Exception as e:
        print(f"Test 3 Failed: Could not click register link. Error: {e}")

    # Wait for the register page to load
    time.sleep(2)

    # Fill out the registration form
    try:
        username_input = driver.find_element(By.NAME, 'username')
        email_input = driver.find_element(By.NAME, 'email')
        password_input = driver.find_element(By.NAME, 'password')

        email_input.clear()
        username_input.clear()
        password_input.clear()

        email_input.send_keys("test2@example.com")
        username_input.send_keys("Test Account 2")
        password_input.send_keys("123456")
        print("Test 4 Passed: Entered registration information.")
    except Exception as e:
        print(f"Test 4 Failed: Could not enter registration information. Error: {e}")

    # Submit the registration form
    try:
        register_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        register_button.click()
        print("Test 5 Passed: Registration form submitted.")
    except Exception as e:
        print(f"Test 5 Failed: Could not submit registration form. Error: {e}")

    # Wait for the login page to load again
    time.sleep(2)

    # Fill out the login form with the newly registered credentials
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'email'))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'password'))
        )
        print("Found email and password input fields on login page.")
    except Exception as e:
        print(f"Test 6 Failed: Could not find email and/or password input fields on login page. Error: {e}")

    try:
        email_input.clear()
        password_input.clear()
        email_input.send_keys("test@example.com")
        password_input.send_keys("123456")
        print("Test 6 Passed: Entered login credentials for newly registered user.")
    except Exception as e:
        print(f"Test 6 Failed: Could not enter login credentials for newly registered user. Error: {e}")

    # Submit the login form
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()
        print("Test 7 Passed: Login form submitted.")
    except Exception as e:
        print(f"Test 7 Failed: Could not submit login form. Error: {e}")

    # Wait for the dashboard to load
    time.sleep(5)

    # Test: Check the dashboard page title
    try:
        assert "Dashboard" in driver.title
        print("Test 8 Passed: Dashboard title is correct.")
    except AssertionError:
        print("Test 8 Failed: Dashboard title is incorrect.")

finally:
    # Close the browser
    driver.quit()
