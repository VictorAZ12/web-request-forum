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
            EC.element_to_be_clickable((By.ID, 'login-link'))
        )
        login_link.click()
        print("Test 2 Passed: Login link clicked successfully.")
    except Exception as e:
        print(f"Test 2 Failed: Could not click login link. Error: {e}")
    
    # Wait for the login form to be displayed
    time.sleep(2)
    
    # Function to test login
    def test_login(email, password):
        # Find the email and password input fields
        try:
            email_input = driver.find_element(By.NAME, 'email')
            password_input = driver.find_element(By.NAME, 'password')
            print("Found email and password input fields.")
        except Exception as e:
            print(f"Could not find email and/or password input fields. Error: {e}")
            return False
        
        # Clear any existing text in the fields
        email_input.clear()
        password_input.clear()
        
        # Enter the login credentials
        try:
            email_input.send_keys(email)
            password_input.send_keys(password)
            print("Entered login credentials.")
        except Exception as e:
            print(f"Could not enter login credentials. Error: {e}")
            return False
        
        # Submit the login form
        try:
            login_form = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_form.click()
            print("Login form submitted.")
        except Exception as e:
            print(f"Could not submit login form. Error: {e}")
            return False
        
        # Wait for the response and check if the login was successful
        time.sleep(5)
        
        # Check if there's any error message displayed
        try:
            error_message = driver.find_element(By.CLASS_NAME, 'flashes').text
            if error_message:
                print(f"Login failed with error: {error_message}")
                return False
        except Exception:
            pass
        
        try:
            if driver.current_url == "http://127.0.0.1:5000/dashboard":
                print("Login successful.")
                return True
            else:
                print("Login failed.")
                return False
        except Exception as e:
            print(f"Error checking login status. Error: {e}")
            return False
            
    # Test login with incorrect credentials
    if not test_login("hoanghung.hr93@gmail.com", "wrongpassword"):
        print("Test 3 Passed: Login with incorrect credentials failed as expected.")
    else:
        print("Test 3 Failed: Login with incorrect credentials should have failed but didn't.")
    

    # Test login with correct credentials
    if test_login("test@example.com", "123456"):
        print("Test 4 Passed: Login with correct credentials successful.")
    else:
        print("Test 4 Failed: Login with correct credentials failed.")
    

finally:
    # Close the browser
    driver.quit()
