// JavaScript for handling settings functionality

document.addEventListener('DOMContentLoaded', function() {
    loadCurrentUserInfo();
});

function loadCurrentUserInfo() {
    // Load current user information
    document.getElementById('username').textContent = currentUser.username;
    document.getElementById('currentEmail').textContent = currentUser.email;
    document.getElementById('profileImageDisplay').src = currentUser.profileImage;
}

function enableEdit() {
    document.getElementById('currentInfo').style.display = 'none';
    document.getElementById('settingsForm').style.display = 'block';
}

function disableEdit() {
    document.getElementById('currentInfo').style.display = 'block';
    document.getElementById('settingsForm').style.display = 'none';
}

document.getElementById('settingsForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Handle profile image change
    const profileImage = document.getElementById('profileImage').files[0];
    if (profileImage) {
        console.log('Profile image selected:', profileImage.name);
        document.getElementById('profileImageDisplay').src = URL.createObjectURL(profileImage);
    }

    // Handle email change
    const email = document.getElementById('email').value;
    if (email) {
        console.log('Email:', email);
        document.getElementById('currentEmail').textContent = email;
    }

    // Handle password change
    const password = document.getElementById('password').value;
    if (password) {
        console.log('Password changed');
    }

    alert('Changes saved successfully!');
    disableEdit();
    loadCurrentUserInfo(); // Reload user info with updated data
});

function logout() {
    // Redirect to login page
    window.location.href = 'HabitNest.html#login-section';
}
