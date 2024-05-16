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
        e.preventDefault();
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    });

    // Event listener for returning to login form from registration form
    backToLoginLink.addEventListener('click', function (e) {
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
});

// Function for handling "Get Started" button click
function handleGetStartedClick(e) {
    e.preventDefault();
    homeSection.style.display = 'none';
    loginSection.style.display = 'block';
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
}
