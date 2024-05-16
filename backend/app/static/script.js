document.addEventListener('DOMContentLoaded', function() {
    loadHabits();
    setMinDate(); // Ensure the min date is set when the page loads
});

function getCSRFToken() {
    return document.querySelector('input[name="csrf_token"]').value;
}

function loadHabits() {
    fetch('/api/habits', {
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(habit => {
            addHabitToDOM(habit.habitname, habit.goal, habit.unit, habit.startDate, 'habitsContainer', habit.hid);
        });
    })
    .catch(error => console.error('Error loading habits:', error));
}

// Set the minimum date for the start date input to today
function setMinDate() {
    var today = new Date().toISOString().split('T')[0];
    document.getElementById('habitStartDate').setAttribute('min', today);
}

// Update unit based on selected habit
document.getElementById('habitName').addEventListener('change', function() {
    var selectedOption = this.options[this.selectedIndex];
    var unit = selectedOption.getAttribute('data-unit');
    document.getElementById('habitUnit').value = unit;
});

// Handle form submission
document.getElementById('newHabitForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = document.getElementById('habitName').value;
    const goal = document.getElementById('habitGoal').value;
    const unit = document.getElementById('habitUnit').value;
    const startDate = document.getElementById('habitStartDate').value;
    const today = new Date().toISOString().split('T')[0];

    if (!startDate) {
        alert('Please select a start date.');
        return;
    }

    if (startDate < today) {
        alert('Please select a date that is not in the past.');
        return;
    }

    if (this.dataset.isEdit === 'true') {
        const habitId = this.dataset.habitId;
        updateHabit(habitId, name, goal, unit, startDate);
    } else {
        addHabit(name, goal, unit, startDate);
    }
    closeModal();
});

function addHabit(name, goal, unit, startDate) {
    fetch('/api/habits', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            habitname: name,
            goal: goal,
            unit: unit,
            startDate: startDate
        })
    })
    .then(response => response.json())
    .then(data => {
        addHabitToDOM(data.habitname, data.goal, data.unit, data.startDate, 'habitsContainer', data.hid);
    })
    .catch(error => console.error('Error adding habit:', error));
}

function addHabitToDOM(name, goal, unit, startDate, containerId, habitId) {
    const container = document.getElementById(containerId);
    const habitDiv = document.createElement('div');
    habitDiv.className = 'habit';
    habitDiv.id = habitId;
    habitDiv.dataset.goal = goal;
    habitDiv.dataset.unit = unit;
    habitDiv.dataset.startDate = startDate;
    habitDiv.dataset.habitId = habitId;
    habitDiv.innerHTML = `
        <div class="habit-details">
            <div class="habit-name">${name}</div>
            <div class="habit-progress">0 / ${goal} ${unit}</div>
            <span class="habit-toggle">⮟</span>
        </div>
        <div class="habit-actions hidden">
            <button class="check-in-btn">Check-In</button>
            <button class="fail-btn">Fail</button>
            <button class="edit-btn" onclick="editHabit(this)">Edit</button>
            <button class="view-progress-btn">View Progress</button>
        </div>
    `;
    setupHabitButtons(habitDiv);
    container.appendChild(habitDiv);
    updateVisibility(containerId);
}

function setupHabitButtons(habitDiv) {
    const details = habitDiv.querySelector('.habit-details');
    details.querySelector('.habit-toggle').addEventListener('click', function() {
        this.parentNode.nextElementSibling.classList.toggle('hidden');
    });

    const actions = habitDiv.querySelector('.habit-actions');
    actions.querySelector('.check-in-btn').addEventListener('click', function() {
        moveHabit(habitDiv, 'successContainer', true);
    });

    actions.querySelector('.fail-btn').addEventListener('click', function() {
        moveHabit(habitDiv, 'failContainer', false);
    });

    actions.querySelector('.edit-btn').addEventListener('click', function() {
        const name = habitDiv.querySelector('.habit-name').textContent;
        const progress = habitDiv.querySelector('.habit-progress').textContent.split('/');
        const goal = progress[1].trim().split(' ')[0];
        const unit = progress[1].trim().split(' ')[1];
        const startDate = habitDiv.dataset.startDate;

        showModal();
        document.getElementById('habitName').value = name;
        document.getElementById('habitGoal').value = goal;
        document.getElementById('habitUnit').value = unit;
        document.getElementById('habitStartDate').value = startDate;
        document.getElementById('newHabitForm').dataset.isEdit = 'true';
        document.getElementById('newHabitForm').dataset.habitId = habitDiv.id;
        document.getElementById('delete-btn').classList.remove('hidden'); // Show delete button when editing
    });

    actions.querySelector('.view-progress-btn').addEventListener('click', function() {
        alert('View progress functionality to be implemented');
    });
}

function updateHabit(habitId, name, goal, unit, startDate) {
    fetch(`/api/habits/${habitId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            habitname: name,
            goal: goal,
            unit: unit,
            startDate: startDate
        })
    })
    .then(response => response.json())
    .then(data => {
        const habitDiv = document.getElementById(habitId);
        habitDiv.querySelector('.habit-name').textContent = name;
        habitDiv.querySelector('.habit-progress').textContent = `0 / ${goal} ${unit}`;
        habitDiv.dataset.goal = goal;
        habitDiv.dataset.unit = unit;
        habitDiv.dataset.startDate = startDate;
        updateVisibility('habitsContainer');
    })
    .catch(error => console.error('Error updating habit:', error));
}

function deleteHabit() {
    const habitId = document.getElementById('newHabitForm').dataset.habitId;
    fetch(`/api/habits/${habitId}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(() => {
        const habitDiv = document.getElementById(habitId);
        habitDiv.parentNode.removeChild(habitDiv);
        closeModal();
        updateVisibility('habitsContainer');
        updateVisibility('successContainer');
        updateVisibility('failContainer');
    })
    .catch(error => console.error('Error deleting habit:', error));
}

function moveHabit(habitDiv, targetContainerId, isSuccess) {
    const targetContainer = document.getElementById(targetContainerId);
    const goal = habitDiv.dataset.goal;
    const unit = habitDiv.dataset.unit;
    habitDiv.querySelector('.habit-progress').textContent = `${isSuccess ? goal : 0} / ${goal} ${unit}`;
    targetContainer.appendChild(habitDiv);
    updateVisibility(targetContainerId);
    updateVisibility('habitsContainer');
}

function updateVisibility(containerId) {
    const container = document.getElementById(containerId);
    container.style.display = container.children.length > 0 ? 'block' : 'none';
}

function showModal() {
    document.getElementById('habitModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('habitModal').style.display = 'none';
    document.getElementById('newHabitForm').reset();
    document.getElementById('newHabitForm').removeAttribute('data-is-edit');
    document.getElementById('newHabitForm').removeAttribute('data-habit-id');
    document.getElementById('delete-btn').classList.add('hidden'); // Hide delete button after closing
}
