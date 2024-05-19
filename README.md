# Project Group
Group Members:
- Hung Hoang (22321855)
- Jiaqi Li (24062188)
- Nikhil Sawant(23882972)
- Yanchen Zhao (23453469)

# Project Introduction
HabitNest is a web-based platform designed to enhance productivity and personal growth through habit tracking and community support. Users can create accounts to set personal goals, track their progress in developing new habits, and participate in community challenges. Habitat fosters a supportive network where users can share tips, celebrate achievements, and find motivation in a like-minded community.  
## Key features
- User account creation and management: Secure login and personal dashboard customization.
- Habit tracking: Users can create, manage, and track daily habits with progress visualization (e.g., streaks, graphs).
- Community challenges: Users can join or create challenges related to common goals, such as "30 days of fitness" or "daily meditation," and track collective progress.
- Reward system: Points or badges awarded for consistency and participation in community goals.
- Social interaction: Users can follow each other, share progress, and send encouragement.
## Deployment
1. Clone the repository to your local machine.
    ```console
    git clone https://github.com/VictorAZ12/web-request-forum`
    ```
2. Navigate to the backend folder, then follow the README.md in the folder to deploy.
## Implementation
### Front end
- Engaging Interface: Modern and motivational design with interactive elements like progress bars and achievement unlock animations.

- Mobile-responsive design: Utilizing Bootstrap for a consistent experience on desktop and mobile devices.

- Real-time updates: Using JavaScript and AJAX for dynamic updates to user dashboards and challenge pages without needing to reload the page.
### Back end
- Flask: Managing server-side logic, user sessions, and data handling.

- SQLite: Storing user profiles, habits, and community challenge data.

- Secure authentication: Implementing Flask extensions for handling secure user authentication and registration processes.
## Testing Instructions
### Front end
- Environment Setup for Testing
Install Selenium and Chrome WebDriver
Ensure you have Python installed. You can download it from python.org.
Install Selenium using pip:
```console
pip install selenium
```
Download Chrome WebDriver from ChromeDriver - WebDriver for Chrome and ensure it's in a directory included in your system's PATH.

-Project Setup:
Navigate to the project directory
Ensure you have the Flask application running. If not, start it:
```console
flask run
```
Running the Tests
Homepage Test:
Navigate to the directory containing the test script. Run the homepage test script:
```console
python test_Selenium_Homepage.py
```

Login Test:
Ensure the Flask application is running and you are in the correct directory.
Run the login test script:
```console
python test_Selenium_Login.py
```
Dashboard Test:
Ensure the Flask application is running and you are in the correct directory.
Run the login test script:
```console
python test_Selenium_Dashboard.py
```

Explanation of Tests
Homepage Test (test_Selenium_Homepage.py):
This test script checks the homepage title, clicks the login link, and verifies the presence of the username and password input fields.
It also attempts to submit the login form and checks the page title after submission.

Registrer (test_Selenium_Register.py):
This test script checks creation of new account.

Login Test (test_Selenium_Login.py):
This test script verifies the login functionality by testing with both correct and incorrect credentials.
For correct credentials, it checks if the user is redirected to the dashboard page.
For incorrect credentials, it checks if the login fails as expected.

Dashboard Test (test_Selenium_Dashboard.py):
This test script verifies the add habit and add challenge functionality.
It also verifies edit habit and delete habit functions. 
It also verifies join/unjoin challenge. 