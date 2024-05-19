var challengeModal = document.getElementById('challengeModal');
var viewChallengeModal = document.getElementById('viewChallengeModal');
var confirmModal = document.getElementById('confirmModal');
var joinedUsers = {};
var selectedChallengeId = null;
document.addEventListener('DOMContentLoaded', function() {
    loadChallenges();
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


// Show the challenge modal
function showChallengeModal() {
    challengeModal.style.display = "block";
}

// Close the challenge modal
function closeChallengeModal() {
    challengeModal.style.display = "none";
    resetChallengeForm();
}


// Handle challenge form submission
document.getElementById('newChallengeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const challengeName = document.getElementById('challengeName').value;
    addChallenge();
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
        addChallengeToDOM(data.id, data.challenge_name, data.description, data.creator_id, data.challenge_goal, 
            data.challenge_unit, data.challenge_frequency, data.challenge_type);
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
            <button id="delete-challenge-btn" class="delete-challenge-btn" onclick="deleteChallenge('${id}')">Delete</button>
        </div>
    `;

    // Toggle challenge actions
    challengeDiv.querySelector('.challenge-toggle').addEventListener('click', function() {
        this.parentNode.nextElementSibling.classList.toggle('hidden');
    });
    
    // control delete button display
    const challengeDeleteButton = challengeDiv.querySelector('.delete-challenge-btn')

    if (document.getElementById('user-id').textContent === String(creator_id)){
        challengeDeleteButton.style.display = 'block';
    } else{
        challengeDeleteButton.remove();
    }

    document.getElementById('allChallenges').appendChild(challengeDiv);


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
        addHabitToDOM(data);
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


// Delete a challenge
function deleteChallenge(challengeId) {
    fetch(`/api/delete_challenge/${challengeId}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(() => {
        const challengeDivId = "challenge" + String(challengeId);
        const challengeDiv = document.getElementById(challengeDivId);
        challengeDiv.remove();
    })
    .catch(error => console.error('Error deleting challenge:', error));
}

// Reset the challenge form
function resetChallengeForm() {
    document.getElementById('newChallengeForm').reset();
    document.getElementById('newChallengeForm').removeAttribute('data-is-edit');
    document.getElementById('newChallengeForm').removeAttribute('data-challenge-id');
    document.getElementById('delete-challenge-btn').classList.add('hidden'); // Hide delete button after closing
}


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