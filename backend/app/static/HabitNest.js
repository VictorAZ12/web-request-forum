document.addEventListener("DOMContentLoaded", function () {
    // Get references to DOM elements
    const loginSection = document.getElementById('login-section');
    const loginLink = document.getElementById('login-link');
    const homeSection = document.getElementById('home-section');
    const homeLink = document.getElementById('home-link');
    const logoLink = document.getElementById('logo-link');
    const getStartedLinks = document.querySelectorAll('#get-started-link');
    const registerLink = document.getElementById('register-link');
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const backToLoginLink = document.getElementById('back-to-login-link');
    const footerHomeLink = document.getElementById('footer-home-link');
    const loginMessageBox = document.getElementById('login-register-error-message')
    // Event listener for showing login section
    loginLink.addEventListener('click', function (e) {
        e.preventDefault();
        homeSection.style.display = 'none';
        loginSection.style.display = 'block';
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    });

    // Event listener for showing home section
    homeLink.addEventListener('click', function (e) {
        e.preventDefault();
        homeSection.style.display = 'block';
        loginSection.style.display = 'none';
    });

    // Event listener for showing home section when logo is clicked
    logoLink.addEventListener('click', function (e) {
        e.preventDefault();
        homeSection.style.display = 'block';
        loginSection.style.display = 'none';
    });

    // Event listeners for "Get Started" links
    getStartedLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            homeSection.style.display = 'none';
            loginSection.style.display = 'block';
            loginForm.style.display = 'block';
            registerForm.style.display = 'none';
        });
    });

    // Event listener for showing registration form
    registerLink.addEventListener('click', function (e) {
        loginMessageBox.style.display = 'none';
        e.preventDefault();
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    });

    // Event listener for returning to login form from registration form
    backToLoginLink.addEventListener('click', function (e) {
        loginMessageBox.style.display = 'none';
        e.preventDefault();
        registerForm.style.display = 'none';
        loginForm.style.display = 'block';
    });

    // Event listener for showing home section from footer link
    footerHomeLink.addEventListener('click', function (e) {
        e.preventDefault();
        homeSection.style.display = 'block';
        loginSection.style.display = 'none';
    });

    // Submit register form
    function handleRegisterFormSubmit(e) {
        e.preventDefault();

        const formData = new FormData(registerForm);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', registerForm.action, true);

        xhr.onload = function () {
            const response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                // Redirect to login section
                loginMessageBox.style.display = 'none';
                loginLink.click();
            } else {
                loginMessageBox.className = 'alert alert-warning'
                loginMessageBox.textContent = response.message;
                loginMessageBox.style.display = 'block';
            }
        };

        xhr.onerror = function () {
            loginMessageBox.className = 'alert alert-danger';
            loginMessageBox.textContent = 'An error occurred. Please try again.';
            loginMessageBox.style.display = 'block';
        };

        xhr.send(formData);
    }
    // Event listener for register form submission
    registerForm.addEventListener('submit', handleRegisterFormSubmit);

    // Function to submit login form
    function handleLoginFormSubmit(e) {
        e.preventDefault();

        const formData = new FormData(loginForm);
        const xhr = new XMLHttpRequest();
        xhr.open('POST', loginForm.action, true);

        xhr.onload = function () {
            const response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                window.location.href = '/dashboard' // redirect to dashboard
            } else {
                loginMessageBox.className = 'alert alert-warning'
                loginMessageBox.textContent = response.message;
                loginMessageBox.style.display = 'block';
            }
        };

        xhr.onerror = function () {
            loginMessageBox.className = 'alert alert-danger';
            loginMessageBox.textContent = 'An error occurred. Please try again.';
            loginMessageBox.style.display = 'block';
        };

        xhr.send(formData);
    }
    // Event listener for form submission
    loginForm.addEventListener('submit', handleLoginFormSubmit);

});

// Function for handling "Get Started" button click
function handleGetStartedClick(e) {
    e.preventDefault();
    homeSection.style.display = 'none';
    loginSection.style.display = 'block';
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
}
