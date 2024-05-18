var challengeModal = document.getElementById('challengeModal');
var viewChallengeModal = document.getElementById('viewChallengeModal');
var confirmModal = document.getElementById('confirmModal');
var joinedUsers = {};
var selectedChallengeId = null;
document.addEventListener('DOMContentLoaded', function() {
    loadChallenges();
    // setMinDateForChallenge();
    loadChallengeTypes();
    
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
            addChallengeToDOM(challenge.id, challenge.challenge_name, challenge.description, challenge.creator_id,
                challenge.challenge_goal, challenge.challenge_unit, challenge.challenge_frequency, challenge.challenge_type);
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



// Set the minimum date for the challenge start date input to today
function setMinDateForChallenge() {
    var today = new Date().toISOString().split('T')[0];
    document.getElementById('challengeStartDate').setAttribute('min', today);
}

// Handle challenge form submission
document.getElementById('newChallengeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const challengeName = document.getElementById('challengeName').value;
    addChallenge();
    // if (this.dataset.isEdit === 'true') {
    //     const challengeId = this.dataset.challengeId;
    //     updateChallenge();
    // } else {
        
    // }
    closeChallengeModal();
});

function addChallenge() {
    const form = document.getElementById('newChallengeForm');
    const formData = new FormData(form);
    fetch('/api/add_challenge', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        //addChallengeToDOM(data.name, data.habit, data.goal, data.unit, data.startDate, data.cid);
    })
    .catch(error => console.error('Error adding challenge:', error));
}

function addChallengeToDOM(id, challengeName, description, creator_id, challengeGoal, challengeUnit,
    challengeFrequency, challenge_type
) {
    const challengeDiv = document.createElement('div');
    const challengeDivId = "challenge" + String(id);
    challengeDiv.className = 'challenge';
    challengeDiv.id = challengeDivId;
    challengeDiv.dataset.challenge_id = id;
    challengeDiv.dataset.name = challengeName;
    challengeDiv.dataset.description = description;
    challengeDiv.dataset.creator_id = creator_id;
    challengeDiv.dataset.goal = challengeGoal;
    challengeDiv.dataset.unit = challengeUnit;
    challengeDiv.dataset.frequency = challengeFrequency;
    challengeDiv.dataset.type = challenge_type;
    const frequencyText = getFrequencyText(challengeFrequency);
    challengeDiv.innerHTML = `
        <div class="challenge-details">
            <div class="challenge-name">${challengeName}:${description}</div>
            <span class="challenge-toggle">&#x22EE;</span>
        </div>
        <div class="challenge-actions hidden">
            <div class="challengeGoal">${challengeGoal} ${challengeUnit} ${frequencyText} </div>
            <button class="join-btn" onclick="joinChallenge('${challengeDivId}')">Join</button>
        </div>
    `;

    // Toggle challenge actions
    challengeDiv.querySelector('.challenge-toggle').addEventListener('click', function() {
        this.parentNode.nextElementSibling.classList.toggle('hidden');
    });

    document.getElementById('allChallenges').appendChild(challengeDiv);


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
    selectedChallengeId = challengeDiv.dataset.challenge_id;
    // remove current listener
    document.getElementById('newHabitForm').removeEventListener('submit', saveHabitHandler);
    // add submit challenge habit listner
    document.getElementById('newHabitForm').addEventListener('submit', saveChallengeHabitHandler);
    

    // Populate the form fields with the dataset values
    document.getElementById('habitType').value = challengeDiv.dataset.type;
    document.getElementById('habitName').value = challengeDiv.dataset.name;
    document.getElementById('habitGoal').value = challengeDiv.dataset.goal;
    document.getElementById('habitUnit').value = challengeDiv.dataset.unit;
    document.getElementById('habitFrequency').value = challengeDiv.dataset.frequency;
    
    // Disable the form fields to make them disabled
    document.getElementById('habitType').disabled = true;
    document.getElementById('habitName').disabled = true;
    document.getElementById('habitGoal').disabled = true;
    document.getElementById('habitUnit').disabled = true;
    document.getElementById('habitFrequency').disabled = true;
    // Enable the start date field
    showHabitModal();
    // Clone the challenge to the habits page
    // addHabitToDOM(challengeName, challengeGoal, challengeUnit, challengeStartDate, 'habitsContainer');

    // challengeDiv.querySelector('.join-btn').classList.add('hidden');
    // challengeDiv.querySelector('.unjoin-btn').classList.remove('hidden');
    // joinedUsers[challengeId]++;
    // alert('Joined the challenge!');
}
function saveChallengeHabit() {
    // enable fields again
    document.getElementById('habitType').disabled = false;
    document.getElementById('habitName').disabled = false;
    document.getElementById('habitGoal').disabled = false;
    document.getElementById('habitUnit').disabled = false;
    document.getElementById('habitFrequency').disabled = false;

    const form = document.getElementById('newHabitForm');
    const formData = new FormData(form);
    fetch(`/api/add_challenge_habit/${selectedChallengeId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        closeHabitModal();
        
    })
    .catch(error => console.error('Error:', error));
    document.getElementById('newHabitForm').removeEventListener('submit', saveChallengeHabitHandler);
    // add submit challenge habit listner
    document.getElementById('newHabitForm').addEventListener('submit', saveHabitHandler);
}

function saveChallengeHabitHandler(event) {
        event.preventDefault();
        saveChallengeHabit();
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

// Initial setup (obsolete)
// document.addEventListener('DOMContentLoaded', function() {
//     setMinDateForChallenge(); // Ensure the min date is set when the page loads
// });

// load challenge types
function loadChallengeTypes() {
    fetch('/api/habit_types')
        .then(response => response.json())
        .then(data => {
            const challengeTypeSelect = document.getElementById('challengeType');
            data.forEach(habitType => {
                const option = document.createElement('option');
                option.value = habitType.id;
                option.textContent = habitType.type;
                challengeTypeSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading challenge types:', error));
}

function getFrequencyText(frequency) {
    switch (frequency) {
        case 1:
            return "per day";
        case 2:
            return "per week";
        case 3:
            return "per month";
        default:
            return "";
    }
}