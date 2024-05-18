var challengeModal = document.getElementById('challengeModal');
var viewChallengeModal = document.getElementById('viewChallengeModal');
var confirmModal = document.getElementById('confirmModal');
var joinedUsers = {};

document.addEventListener('DOMContentLoaded', function() {
    loadChallenges();
    setMinDateForChallenge();
    loadBaseHabits();
});

function getCSRFToken() {
    return document.querySelector('input[name="csrf_token"]').value;
}

function loadChallenges() {
    fetch('/api/challenges', {
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(challenge => {
            addChallengeToDOM(challenge.name, challenge.habit, challenge.goal, challenge.unit, challenge.startDate, challenge.cid);
        });
    })
    .catch(error => console.error('Error loading challenges:', error));
}

function loadBaseHabits() {
    fetch('/api/habits', {
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        const baseHabitSelect = document.getElementById('baseHabit');
        data.forEach(habit => {
            const option = document.createElement('option');
            option.value = habit.id;
            option.textContent = habit.habit_name;
            baseHabitSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error loading base habits:', error));
}

// Show the challenge modal
function showChallengeModal() {
    challengeModal.style.display = "block";
    setMinDateForChallenge();
}

// Close the challenge modal
function closeChallengeModal() {
    challengeModal.style.display = "none";
    resetChallengeForm();
}

// Close the view challenge modal
function closeViewChallengeModal() {
    viewChallengeModal.style.display = "none";
}

// Show confirmation modal
function showConfirmModal(message, onConfirm) {
    document.getElementById('confirmMessage').textContent = message;
    confirmModal.style.display = "block";
    document.getElementById('confirmOkBtn').onclick = function() {
        confirmModal.style.display = "none";
        onConfirm();
    };
    document.getElementById('confirmCancelBtn').onclick = function() {
        confirmModal.style.display = "none";
    };
}

// Set the minimum date for the challenge start date input to today
function setMinDateForChallenge() {
    var today = new Date().toISOString().split('T')[0];
    document.getElementById('challengeStartDate').setAttribute('min', today);
}

// Handle challenge form submission
document.getElementById('newChallengeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const challengeName = document.getElementById('challengeName').value;
    const baseHabit = document.getElementById('baseHabit').value;

    if (this.dataset.isEdit === 'true') {
        const challengeId = this.dataset.challengeId;
        updateChallenge(challengeId, challengeName, baseHabit);
    } else {
        addChallenge(challengeName, baseHabit);
    }
    closeChallengeModal();
});

function addChallenge(challengeName, baseHabit) {
    fetch('/api/challenges', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            name: challengeName,
            base_habit: baseHabit
        })
    })
    .then(response => response.json())
    .then(data => {
        addChallengeToDOM(data.name, data.habit, data.goal, data.unit, data.startDate, data.cid);
    })
    .catch(error => console.error('Error adding challenge:', error));
}

function addChallengeToDOM(challengeName, habitName, challengeGoal, challengeUnit, challengeStartDate, challengeId) {
    const today = new Date().toISOString().split('T')[0];
    const challengeDiv = document.createElement('div');
    challengeDiv.className = 'challenge';
    challengeDiv.id = challengeId;
    challengeDiv.dataset.name = challengeName;
    challengeDiv.dataset.habit = habitName;
    challengeDiv.dataset.goal = challengeGoal;
    challengeDiv.dataset.unit = challengeUnit;
    challengeDiv.dataset.startDate = challengeStartDate;
    challengeDiv.innerHTML = `
        <div class="challenge-details">
            <div class="challenge-name">${challengeName}</div>
            <div class="challenge-goal">${challengeGoal} ${challengeUnit}</div>
            <div class="challenge-start-date">Starts: ${challengeStartDate}</div>
            <div class="challenge-habit">Habit: ${habitName}</div>
            <span class="challenge-toggle">то?</span>
        </div>
        <div class="challenge-actions hidden">
            <button class="join-btn" onclick="confirmJoinChallenge(${challengeId})">Join</button>
            <button class="unjoin-btn hidden" onclick="confirmUnjoinChallenge(${challengeId})">Unjoin</button>
            <button class="edit-btn" onclick="editChallenge(this)">Edit</button>
            <button class="view-btn" onclick="viewChallenge(${challengeId})">View</button>
        </div>
    `;

    // Toggle challenge actions
    challengeDiv.querySelector('.challenge-toggle').addEventListener('click', function() {
        this.parentNode.nextElementSibling.classList.toggle('hidden');
    });

    if (challengeStartDate > today) {
        document.getElementById('futureChallenges').appendChild(challengeDiv);
    } else {
        document.getElementById('activeChallenges').appendChild(challengeDiv);
    }

    joinedUsers[challengeId] = 0; // Initialize the joined users count for the new challenge
}

// Handle confirm join challenge
function confirmJoinChallenge(challengeId) {
    showConfirmModal("Are you sure you want to join this challenge?", function() {
        joinChallenge(challengeId);
    });
}

// Handle confirm unjoin challenge
function confirmUnjoinChallenge(challengeId) {
    showConfirmModal("Are you sure you want to unjoin this challenge?", function() {
        unjoinChallenge(challengeId);
    });
}

// Handle join challenge
function joinChallenge(challengeId) {
    const challengeDiv = document.getElementById(challengeId);
    const challengeName = challengeDiv.dataset.name;
    const habitName = challengeDiv.dataset.habit;
    const challengeGoal = challengeDiv.dataset.goal;
    const challengeUnit = challengeDiv.dataset.unit;
    const challengeStartDate = challengeDiv.dataset.startDate;

    // Clone the challenge to the habits page
    addHabitToDOM(challengeName, challengeGoal, challengeUnit, challengeStartDate, 'habitsContainer');

    challengeDiv.querySelector('.join-btn').classList.add('hidden');
    challengeDiv.querySelector('.unjoin-btn').classList.remove('hidden');
    joinedUsers[challengeId]++;
    alert('Joined the challenge!');
}

// Handle unjoin challenge
function unjoinChallenge(challengeId) {
    // Remove the habit from the habits container
    const habitsContainer = document.getElementById('habitsContainer');
    const habitDivs = habitsContainer.getElementsByClassName('habit');
    for (let i = 0; i < habitDivs.length; i++) {
        const habitDiv = habitDivs[i];
        if (habitDiv.dataset.challengeId === challengeId.toString()) {
            habitsContainer.removeChild(habitDiv);
            break;
        }
    }

    const challengeDiv = document.getElementById(challengeId);
    challengeDiv.querySelector('.join-btn').classList.remove('hidden');
    challengeDiv.querySelector('.unjoin-btn').classList.add('hidden');
    joinedUsers[challengeId]--;
    alert('Unjoined the challenge!');
}

// Handle edit challenge
function editChallenge(button) {
    const challengeDiv = button.closest('.challenge');
    const challengeName = challengeDiv.querySelector('.challenge-name').textContent;
    const challengeGoal = challengeDiv.querySelector('.challenge-goal').textContent.split(' ')[0];
    const challengeUnit = challengeDiv.querySelector('.challenge-goal').textContent.split(' ')[1];
    const challengeStartDate = challengeDiv.querySelector('.challenge-start-date').textContent.split(': ')[1];
    const habitName = challengeDiv.querySelector('.challenge-habit').textContent.split(': ')[1];

    showChallengeModal();
    document.getElementById('challengeName').value = challengeName;
    document.getElementById('baseHabit').value = habitName;
    document.getElementById('challengeGoal').value = challengeGoal;
    document.getElementById('challengeUnit').value = challengeUnit;
    document.getElementById('challengeStartDate').value = challengeStartDate;
    document.getElementById('newChallengeForm').dataset.isEdit = 'true';
    document.getElementById('newChallengeForm').dataset.challengeId = challengeDiv.id;
    document.getElementById('delete-challenge-btn').classList.remove('hidden'); // Show delete button when editing
}

// Handle view challenge
function viewChallenge(challengeId) {
    const challengeDiv = document.getElementById(challengeId);
    const challengeName = challengeDiv.dataset.name;
    const habitName = challengeDiv.dataset.habit;
    const challengeGoal = challengeDiv.dataset.goal;
    const challengeUnit = challengeDiv.dataset.unit;
    const challengeStartDate = challengeDiv.dataset.startDate;
    const joinedCount = joinedUsers[challengeId] || 0;

    const details = `
        <p>Challenge: ${challengeName}</p>
        <p>Habit: ${habitName}</p>
        <p>Goal: ${challengeGoal} ${challengeUnit}</p>
        <p>Start Date: ${challengeStartDate}</p>
        <p>Users Joined: ${joinedCount}</p>
    `;
    document.getElementById('viewChallengeDetails').innerHTML = details;
    viewChallengeModal.style.display = 'block';
}

// Update a challenge
function updateChallenge(challengeId, name, baseHabit) {
    fetch(`/api/challenges/${challengeId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            name: name,
            base_habit: baseHabit
        })
    })
    .then(response => response.json())
    .then(data => {
        const challengeDiv = document.getElementById(challengeId);
        challengeDiv.querySelector('.challenge-name').textContent = name;
        challengeDiv.dataset.name = name;
        challengeDiv.dataset.habit = baseHabit;
    })
    .catch(error => console.error('Error updating challenge:', error));
}

// Delete a challenge
function deleteChallenge() {
    const challengeId = document.getElementById('newChallengeForm').dataset.challengeId;
    fetch(`/api/challenges/${challengeId}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(() => {
        const challengeDiv = document.getElementById(challengeId);
        challengeDiv.parentNode.removeChild(challengeDiv);
        closeChallengeModal();
    })
    .catch(error => console.error('Error deleting challenge:', error));
}

// // Add a habit to the DOM (reuse function from habit management script)
// function addHabitToDOM(name, goal, unit, startDate, containerId) {
//     const container = document.getElementById(containerId);
//     const habitId = Date.now();  // Using current timestamp as unique ID
//     const habitDiv = document.createElement('div');
//     habitDiv.className = 'habit';
//     habitDiv.id = habitId;
//     habitDiv.dataset.goal = goal;
//     habitDiv.dataset.unit = unit;
//     habitDiv.dataset.startDate = startDate;
//     habitDiv.dataset.challengeId = containerId === 'habitsContainer' ? habitId : ''; // Set challengeId for habits added from challenges
//     habitDiv.innerHTML = `
//         <div class="habit-details">
//             <div class="habit-name">${name}</div>
//             <div class="habit-progress">0 / ${goal} ${unit}</div>
//             <span class="habit-toggle">то?</span>
//         </div>
//         <div class="habit-actions hidden">
//             <button class="check-in-btn">Check-In</button>
//             <button class="fail-btn">Fail</button>
//             <button class="edit-btn" onclick="editHabit(this)">Edit</button>
//             <button class="view-progress-btn">View Progress</button>
//         </div>
//     `;
//     setupHabitButtons(habitDiv);
//     container.appendChild(habitDiv);
//     updateVisibility(containerId);
// }

// Reset the challenge form
function resetChallengeForm() {
    document.getElementById('newChallengeForm').reset();
    document.getElementById('newChallengeForm').removeAttribute('data-is-edit');
    document.getElementById('newChallengeForm').removeAttribute('data-challenge-id');
    document.getElementById('delete-challenge-btn').classList.add('hidden'); // Hide delete button after closing
}

// Initial setup
document.addEventListener('DOMContentLoaded', function() {
    setMinDateForChallenge(); // Ensure the min date is set when the page loads
});
