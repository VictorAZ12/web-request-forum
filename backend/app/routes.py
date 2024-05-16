from flask import redirect, url_for, request, jsonify, flash, render_template
from app import app, db, bcrypt
from app.models import User, UserChallenge, Challenge, Habit
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm, HabitForm, ChallengeForm
# Pages
@app.route('/')
@login_required
def home():
    """Returns homepage html"""
    flash("Welcome to web app homepage!")
    return "Welcome to web app homepage!"

# Test only login protected page
@app.route('/protected')
@login_required
def protected():
    return "You're logged in and can access this protected page"

@app.route('/register', methods=['POST'])
def register():
    """Register route"""
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        username = register_form.username.data
        password = register_form.password.data
        # check existence
        existing_email_user = User.query.filter_by(email=email).first()
        if existing_email_user:
            return "Email exists!"
        existing_username_user = User.query.filter_by(username=username).first()
        if existing_username_user:
            return "Username exists!"

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, username=username, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return('Your account has been created! You can now log in', 'success')


@app.route('/login', methods=['POST'])
def login():
    """Login route"""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        # check existence
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.hashed_password, password):
            login_user(user)
            return redirect(url_for('protected'))
        else:
            return 'Login Unsuccessful. Please check email and password'



@app.route('/index', methods=['GET', 'POST'])
def index():
    """Index page with login and register forms"""
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template('HabitNest.html', login_form = login_form, register_form = register_form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    habit_form = HabitForm()
    challenge_form = ChallengeForm()
    return render_template('Dashboard.html', 
                           habit_form = habit_form,
                           challenge_form = challenge_form)

@app.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')

# APIs
@app.route('/api/habits', methods=['GET'])
@login_required
def get_habits():
    """Retrieve all habits of current user"""
    user_id = current_user.get_id()
    user_habits = Habit.query.filter_by(user_id=user_id).all()
    result = []
    for habit in user_habits:
        result.append({
            "user_id": habit.user_id,
            "habit_name": habit.habit_name,
            "description": habit.description,
            "target_date": habit.target_date,
        })
    return jsonify(result)

@app.route('/api/add_habit', methods=['POST'])
@login_required
def add_habit():
    habit_form = HabitForm()
    if habit_form.validate_on_submit():
        habit_name = habit_form.habit_name.data
        description = habit_form.description.data
        target_date = habit_form.target_date.data
        habit = Habit(user_id=current_user.get_id(),
                      habit_name=habit_name,
                      description=description,
                      target_date=target_date)
        db.session.add(habit)
        db.session.commit()
        return redirect(url_for("dashboard"))

@app.route('/api/challenges', methods=['GET'])
@login_required
def get_challenges():
    """Retrieve all challenges: public and user's private ones"""
    user_id = current_user.get_id()
    created_challenges = Challenge.query.filter_by(creator_id=user_id).all()
    public_challenges = Challenge.query.filter_by(public=True).all()
    user_challenges = created_challenges + public_challenges
    result = []
    existing_challenges = []
    for challenge in user_challenges:
        if challenge.id not in existing_challenges:
            result.append({
                "id": challenge.id,
                "name": challenge.name,
                "content": challenge.content,
                "public": challenge.public,
                "modifiable": str(challenge.creator_id) == str(user_id)
            })
            existing_challenges.append(challenge.id)

    return jsonify(result)

@app.route('/api/add_challenge', methods=['POST'])
@login_required
def add_challenge():
    challenge_form = ChallengeForm()
    if challenge_form.validate_on_submit():
        challenge_name = challenge_form.challenge_name.data
        content = challenge_form.content.data
        public = challenge_form.public.data
        challenge = Challenge(creator_id=current_user.get_id(),
                          name=challenge_name,
                          content=content,
                          public=public)
        db.session.add(challenge)
        db.session.commit()
        return redirect(url_for("dashboard"))

@app.route('/api/users', methods=['GET'])
def get_users():
    ''' Get list of all users '''
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    print(users_list)
    return jsonify(users_list)

@app.route('/api/user_challenge/', methods=['GET'])
def get_user_challenges():
    ''' Get list of challenges related to a user '''
    uid = request.args.get('uid')
    if not uid:
        return jsonify({'error': 'User ID (uid) is required'}), 400

    user = User.query.get(uid)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_challenges = [uc.challenge_id for uc in UserChallenge.query.filter_by(user_id=uid).all()]
    return jsonify(user_challenges)
