from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome WebDriver with a specified window size
driver = webdriver.Chrome()

def test_login(email, password):
    driver.get("http://127.0.0.1:5000/index")
    driver.maximize_window()
    # Click login link
    try:
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'login-link'))
        )
        login_link.click()
        print("Login link clicked.")
    except Exception as e:
        print(f"Could not click login link. Error: {e}")
        return False
    
    # Find the email and password input fields
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        password_input = driver.find_element(By.NAME, 'password')
        print("Found email and password input fields.")
    except Exception as e:
        print(f"Could not find email and/or password input fields. Error: {e}")
        return False
    
    # Clear any existing text in the fields
    try:
        email_input.clear()
        password_input.clear()
        print("Cleared input fields.")
    except Exception as e:
        print(f"Could not clear input fields. Error: {e}")
        return False
    
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
    
    # Wait for the dashboard to load and check URL
    try:
        WebDriverWait(driver, 10).until(
            EC.url_contains("/dashboard")
        )
        print("Login successful.")
        return True
    except Exception as e:
        print(f"Login failed. Error: {e}")
        return False

def test_create_habit(driver):
    # Click add habit button
    try:
        add_habit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'add-habit-btn'))
        )
        add_habit_button.click()
        print("Add habit button clicked.")
    except Exception as e:
        print(f"Could not click add habit button. Error: {e}")
        return False
    
    # Fill in the habit form
    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'habitName'))
    )
    
  
        driver.find_element(By.ID, 'habitName').send_keys("Running")
        driver.find_element(By.ID, 'habitType').send_keys("Hobby")
        driver.find_element(By.ID, 'habitGoal').send_keys("10")
        driver.find_element(By.ID, 'habitUnit').send_keys("times")
        driver.find_element(By.ID, 'habitFrequency').send_keys("1")
        start_date = driver.find_element(By.ID, 'startDate').send_keys("2024-06-20")
        print("Habit form filled out.")
    except Exception as e:
        print(f"Could not fill out habit form. Error: {e}")
        return False
    
    # Submit the form
    try:
        save_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        save_button.click()
        print("Habit form submitted.")
        return True
    except Exception as e:
        print(f"Could not submit habit form. Error: {e}")
        return False

def test_create_challenge(driver):
    # Click add challenge button
    try:
        add_challenge_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'add-challenge-btn'))
        )
        add_challenge_button.click()
        print("Add challenge button clicked.")
    except Exception as e:
        print(f"Could not click add challenge button. Error: {e}")
        return False
    
    # Fill in the challenge form
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'challengeName'))
    )
    driver.find_element(By.ID, 'challengeName').send_keys("Test Challenge")
    driver.find_element(By.ID, 'challengeType').send_keys("Hobby")
    driver.find_element(By.ID, 'description').send_keys("Test Challenge Description")
    driver.find_element(By.ID, 'challengeGoal').send_keys("10")
    driver.find_element(By.ID, 'challengeUnit').send_keys("times")
    driver.find_element(By.ID, 'challengeFrequency').send_keys("1")
    
    
    # Submit the form
    try:
        save_button = driver.find_element(By.CSS_SELECTOR, 'form#newChallengeForm button[type="submit"]')
        save_button.click()
        time.sleep(2)  # wait for the form to submit and modal to close
        print("Challenge form submitted.")
        return True
    except Exception as e:
        print(f"Could not submit challenge form. Error: {e}")
        return False
        
def test_edit_habit(driver):
    try:
        toggle_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'habit-toggle'))
        )
        toggle_button.click()
        edit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'edit-btn'))
        )
        edit_button.click()
        print("Edit habit button clicked.")
    except Exception as e:
        print(f"Could not click edit habit button. Error: {e}")
        return False
    
    try:
        habit_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'habitName'))
        )
        habit_goal = driver.find_element(By.ID, 'habitGoal')
        habit_name.clear()
        habit_name.send_keys("Read More Books")
        habit_goal.clear()
        habit_goal.send_keys("20")
        print("Habit form edited.")
    except Exception as e:
        print(f"Could not edit habit form. Error: {e}")
        return False
    
    try:
        save_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        save_button.click()
        print("Edited habit form submitted.")
        return True
    except Exception as e:
        print(f"Could not submit edited habit form. Error: {e}")
        return False
        
def test_delete_habit(driver):
    try:
        edit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'edit-btn'))
        )
        edit_button.click()
        print("Edit habit button clicked.")
    except Exception as e:
        print(f"Could not click edit habit button. Error: {e}")
        return False
        
    try:
        # Click the delete button within the habit form
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'delete-btn'))
        )
        delete_button.click()
        print("Delete habit button clicked.")
        return True
    except Exception as e:
        print(f"Could not delete habit. Error: {e}")
        return False
        
# Function to delete a challenge
def test_delete_challenge(driver):
    try:
        toggle_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'challenge-toggle'))
        )
        toggle_button.click()

        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'delete-challenge-btn'))
        )
        delete_button.click()
        print("Delete challenge button clicked.")
        return True
    except Exception as e:
        print(f"Could not click delete challenge button. Error: {e}")
        return False
        
        
def test_join_challenge(driver):
    try:
        # Click the ellipsis button to show the join button
        ellipsis_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'challenge-toggle'))
        )
        ellipsis_button.click()

        # Click the join button for the challenge
        join_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'join-btn'))
        )
        join_button.click()

        # Enter the start date for the challenge
        start_date = driver.find_element(By.ID, 'startDate').send_keys("2024-06-20")

        # Submit the form to join the challenge
        save_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        save_button.click()
        print("Join challenge button clicked.")
        return True
    except Exception as e:
        print(f"Could not join challenge. Error: {e}")
        return False

def test_quit_challenge(driver):
    try:
        # Click the ellipsis button in the active challenges section to show the quit button
        ellipsis_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="activeChallenges"]//span[@class="habit-toggle"]'))
        )
        ellipsis_button.click()

        # Click the quit button for the challenge in the active challenges section
        quit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'quit-challenge-btn'))
        )
        quit_button.click()
        print("Quit challenge button clicked.")
        return True
    except Exception as e:
        print(f"Could not quit challenge. Error: {e}")
        return False

try:
    if test_login("test@example.com", "123456"):
        print("Login successful.")
        time.sleep(2)  # Wait for the dashboard to load
    
        if test_create_habit(driver):
            print("Test 1 Passed: create habit successfully")
            time.sleep(2)
        else:
            print("Test 1 Failed: create habit failed")
        
        if test_create_challenge(driver):
            print("Test 2 Passed: create challenge successfully")
            time.sleep(2)
        else:
            print("Test 2 Failed: create challenge failed")
            
        if test_edit_habit(driver):
            print("Test 3 Passed: Edit form successfully")
            time.sleep(2)
        else:
            print("Test 3 Failed: Edit form failed")
            
        if test_delete_habit(driver):
            print("Test 4 Passed: Delete habit successfully")
            time.sleep(2)
        else:
            print("Test 4 Failed: Delete habit failed")
            
        if test_delete_challenge(driver):
            print("Test 5 Passed: Delete challenge successfully")
            time.sleep(2)
        else:
            print("Test 5 Failed: Delete challenge failed")
            
        if test_join_challenge(driver):
            print("Test 6 Passed: Join challenge successfully")
            time.sleep(2)
        else:
            print("Test 6 Failed: Join challenge failed")
            
        if test_quit_challenge(driver):
            print("Test 7 Passed: Unjoin challenge successfully")
            time.sleep(2)
        else:
            print("Test 7 Failed: Unjoin challenge failed")

    else:
        print("Login failed. Cannot proceed with further tests.")
    
finally:
    driver.quit()
