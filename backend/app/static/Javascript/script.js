document.addEventListener('DOMContentLoaded', function () {
    // Event listeners for opening modals
    document.querySelector('.add-habit-btn').addEventListener('click', function () {
        showHabitModal();
    });
    document.querySelector('.close').addEventListener('click', function () {
        closeHabitModal();
    });

    // Event listeners for form submissions
    document.getElementById('newHabitForm').addEventListener('submit', function (event) {
        event.preventDefault();
        saveHabit();
    });

    // Load existing habits
    loadHabits();
    loadHabitTypes();
});

function setMinDate(elementId) {
    var today = new Date().toISOString().split('T')[0];
    document.getElementById(elementId).setAttribute('min', today);
}

function showHabitModal() {
    document.getElementById('habitModal').style.display = 'block';
    setMinDate('startDate');
}

function closeHabitModal() {
    document.getElementById('habitModal').style.display = 'none';
    document.getElementById('newHabitForm').reset();
    document.getElementById('delete-btn').classList.add('hidden');
}

function loadHabitTypes() {
    fetch('/api/habit_types')
        .then(response => response.json())
        .then(data => {
            const habitTypeSelect = document.getElementById('habitType');
            data.forEach(habitType => {
                const option = document.createElement('option');
                option.value = habitType.id;
                option.textContent = habitType.type;
                habitTypeSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading habit types:', error));
}

// Save a new habit or update an existing one
function saveHabit() {
    const form = document.getElementById('newHabitForm');
    const formData = new FormData(form);
    const habitData = {
        habit_type: formData.get('habitType'),
        habit_name: formData.get('habitName'),
        habit_goal: formData.get('habitGoal'),
        habit_unit: formData.get('habitUnit'),
        habit_frequency: formData.get('habitFrequency'),
        start_date: formData.get('startDate')
    };

    const isEdit = form.dataset.isEdit === 'true';
    const habitId = form.dataset.habitId;

    fetch(isEdit ? `/api/habits/${habitId}` : '/api/add_habit', {
        method: isEdit ? 'PUT' : 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(habitData)
    })
    .then(response => response.json())
    .then(data => {
        if (isEdit) {
            updateHabitInDOM(data);
        } else {
            addHabitToDOM(data);
        }
        closeHabitModal();
    })
    .catch(error => console.error('Error:', error));
}

// Add a habit to the DOM
function addHabitToDOM(habit) {
    const container = document.getElementById('habitsContainer');
    const habitDiv = document.createElement('div');
    habitDiv.className = 'habit';
    habitDiv.id = habit.id;
    habitDiv.innerHTML = `
        <div class="habit-details">
            <div class="habit-name">${habit.habit_name}</div>
            <div class="habit-progress">0 / ${habit.habit_goal} ${habit.habit_unit}</div>
            <span class="habit-toggle">�?</span>
        </div>
        <div class="habit-actions hidden">
            <button class="check-in-btn">Check-In</button>
            <button class="fail-btn">Fail</button>
            <button class="edit-btn">Edit</button>
            <button class="view-progress-btn">View Progress</button>
        </div>
    `;
    setupHabitButtons(habitDiv);
    container.appendChild(habitDiv);
}

// Update a habit in the DOM
function updateHabitInDOM(habit) {
    const habitDiv = document.getElementById(habit.id);
    habitDiv.querySelector('.habit-name').textContent = habit.habit_name;
    habitDiv.querySelector('.habit-progress').textContent = `0 / ${habit.habit_goal} ${habit.habit_unit}`;
}

// Additional functions and event listeners

function setMinDate(elementId) {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById(elementId).setAttribute('min', today);
}

function showHabitModal() {
    document.getElementById('habitModal').style.display = 'block';
    setMinDate('startDate');
}

function closeHabitModal() {
    document.getElementById('habitModal').style.display = 'none';
    document.getElementById('newHabitForm').reset();
    document.getElementById('delete-btn').classList.add('hidden');
    delete document.getElementById('newHabitForm').dataset.isEdit;
    delete document.getElementById('newHabitForm').dataset.habitId;
}

function setupHabitButtons(habitDiv) {
    habitDiv.querySelector('.habit-toggle').addEventListener('click', function () {
        habitDiv.querySelector('.habit-actions').classList.toggle('hidden');
    });

    habitDiv.querySelector('.edit-btn').addEventListener('click', function () {
        editHabit(habitDiv);
    });

    habitDiv.querySelector('.check-in-btn').addEventListener('click', function () {
        checkInHabit(habitDiv);
    });

    habitDiv.querySelector('.fail-btn').addEventListener('click', function () {
        failHabit(habitDiv);
    });

    habitDiv.querySelector('.view-progress-btn').addEventListener('click', function () {
        viewHabitProgress(habitDiv);
    });
}

function editHabit(habitDiv) {
    const habitId = habitDiv.id;
    fetch(`/api/habits/${habitId}`)
        .then(response => response.json())
        .then(data => {
            const form = document.getElementById('newHabitForm');
            form.csrf_token.value = getCSRFToken();
            form.habitType.value = data.habit_type;
            form.habitName.value = data.habit_name;
            form.habitGoal.value = data.habit_goal;
            form.habitUnit.value = data.habit_unit;
            form.habitFrequency.value = data.habit_frequency;
            form.startDate.value = data.start_date;
            form.dataset.habitId = habitId;
            form.dataset.isEdit = 'true';
            document.getElementById('habitModal').style.display = 'block';
            document.getElementById('delete-btn').classList.remove('hidden');
        })
        .catch(error => console.error('Error:', error));
}

function checkInHabit(habitDiv) {
    const habitId = habitDiv.id;
    fetch(`/api/habits/${habitId}/checkin`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        const progress = habitDiv.querySelector('.habit-progress');
        progress.textContent = `${data.completed} / ${data.goal} ${data.unit}`;
    })
    .catch(error => console.error('Error checking in habit:', error));
}

function failHabit(habitDiv) {
    const habitId = habitDiv.id;
    fetch(`/api/habits/${habitId}/fail`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        const progress = habitDiv.querySelector('.habit-progress');
        progress.textContent = `0 / ${data.goal} ${data.unit}`;
    })
    .catch(error => console.error('Error failing habit:', error));
}

function viewHabitProgress(habitDiv) {
    const habitId = habitDiv.id;
    fetch(`/api/habits/${habitId}/progress`)
    .then(response => response.json())
    .then(data => {
        alert(`Habit Progress:\nCompleted: ${data.completed}\nGoal: ${data.goal}\nUnit: ${data.unit}`);
    })
    .catch(error => console.error('Error viewing habit progress:', error));
}

function loadHabits() {
    fetch('/api/habits')
        .then(response => response.json())
        .then(data => {
            data.forEach(habit => addHabitToDOM(habit));
        })
        .catch(error => console.error('Error loading habits:', error));
}

function getCSRFToken() {
    return document.querySelector('input[name="csrf_token"]').value;
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
        closeHabitModal();
    })
    .catch(error => console.error('Error deleting habit:', error));
}

