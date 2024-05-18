from flask import redirect, url_for, request, jsonify, flash, render_template
from app import app, db, bcrypt
from app.models import User, UserChallenge, Challenge, Habit, HabitType, Follow, Comment, Tip, UserChallenge, HabitRecord
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm, HabitForm, ChallengeForm, CSRFForm, ChallengeToHabitForm
from datetime import datetime, timedelta
import calendar
# Pages
@app.route('/')
@login_required
def home():
    """Returns homepage html"""
    return "Welcome to web app homepage!"

@app.route('/register', methods=['POST'])
def register():
    """Register route"""
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        username = register_form.username.data
        password = register_form.password.data
        # validate availability
        existing_email_user = User.query.filter_by(email=email).first()
        if existing_email_user:
            return jsonify({'status':'error', 'message':'Email already registered.'}), 400
        existing_username_user = User.query.filter_by(username=username).first()
        if existing_username_user:
            return jsonify({'status':'error', 'message':'username occupied.'}), 400
        # create a new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, username=username, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user) # login user
        return jsonify({'status':'success', 'message':'account registered successfully.'}), 201
    else:
        return jsonify({'status':'error', 'message':'form data invalid'}), 400


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
            return jsonify({'status':'success', 'message':'logged in successfully'}), 200
        else:
            return jsonify({'status':'error', 'message': 'login unsuccessful, please check email and password'}), 401
    else:
        return jsonify({'status':'error', 'message':'form data invalid'}), 400



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
@login_required
def dashboard():
    habit_form = HabitForm()
    challenge_form = ChallengeForm()
    return render_template('Dashboard.html', 
                           habit_form = habit_form,
                           challenge_form = challenge_form,
                           user = current_user)

@app.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')

# APIs
@app.route('/api/habit_types', methods=['GET'])
@login_required
def get_habit_types():
    """Retrieve all habit types"""
    habit_types = HabitType.query.all()
    result = []
    for habit_type in habit_types:
        result.append(habit_type.to_dic())
    return jsonify(result)


@app.route('/api/habits', defaults={'habit_id': None}, methods=['GET'])
@app.route('/api/habits/<int:habit_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_habits(habit_id):
    """Retrieve all habits of current user or a specific habit"""
    user_id = current_user.get_id()
    if request.method == 'GET':
        if habit_id is None:
            user_habits = Habit.query.filter_by(user_id=user_id).all()
            result = []
            for habit in user_habits:
                result.append(habit.to_dict())
            return jsonify(result), 200
        else:
            habit = Habit.query.filter_by(user_id=user_id, id=habit_id).first()
            if habit:
                return jsonify(habit.to_dict())
            else:
                return jsonify({'status':'error', 'message':'Habit not found'}), 404
    if request.method == 'PUT':
        habit_form = HabitForm()
        habit = Habit.query.filter_by(id=habit_id, user_id=current_user.get_id()).first()
        if habit:
            habit.habit_name = habit_form.habitName.data
            habit.start_date = habit_form.startDate.data
            habit.habit_goal = habit_form.habitGoal.data
            habit.habit_unit = habit_form.habitUnit.data
            habit.habit_frequency = habit_form.habitFrequency.data
            habit.habit_type = habit_form.habitType.data
            db.session.commit()
            return jsonify(habit.to_dict()), 201
        else:
            return jsonify({'status':'error', 'message':'Habit not found'}), 404
    if request.method == 'DELETE':
        habit = Habit.query.filter_by(id=habit_id, user_id=current_user.get_id()).first()
        if habit is not None:
            try:
                db.session.delete(habit)
                db.session.commit()
                return jsonify({'status':'success', 'message':'Habit deleted.'}), 200
            except:
                 return jsonify({'status':'error', 'message':'Something is wrong.'}), 500
        else:
            return jsonify({'status':'error', 'message':'Habit not found'}), 404
        

@app.route('/api/habits/checkin/<int:habit_id>', methods = ['GET', 'POST'])
def check_in(habit_id):
    if request.method == 'GET':
        habit_records = HabitRecord.query.filter_by(habit=habit_id).all()
        result = []
        for habit_record in habit_records:
            result.append(str(habit_record.record_date))
        return jsonify(result), 200
    if request.method == 'POST':
        habit = Habit.query.filter_by(id=habit_id).first()
        if habit is None:
            return jsonify({'status':'error', 'message':'Habit not found'}), 404
        user_id = current_user.get_id()
        if str(habit.user_id) != str(user_id):
            return jsonify({'status':'error', 'message':'Not your habit'}), 404
        record_date = datetime.now()
        habit_record = HabitRecord(record_date=record_date,
                                   habit=habit_id)
        # add record
        db.session.add(habit_record)
        db.session.commit()
        # check progress
        progress = check_progress(habit_id)
        if progress is not None:
            return jsonify({'status':'success', 
                            'message':'Check-in done',
                            'completed': progress["completed"],
                            'goal': habit.habit_goal,
                            'unit': habit.habit_unit
                            }), 200
        else:
            return jsonify({'status':'error', 'message':'Something went wrong'}), 400
        
@app.route('/api/habits/progress/<int:habit_id>', methods = ['GET'])
@login_required
def view_progress(habit_id):
    if request.method == 'GET':
        habit = Habit.query.filter_by(id=habit_id).first()
        if habit is None:
            return jsonify({'status':'error', 'message':'Habit not found'}), 404
        
        if str(current_user.get_id()) != str(habit.user_id):
            return jsonify({'status':'error', 'message':'Not your habit'}), 401
        
        progress = check_progress(habit_id)
        if progress is not None:
            return jsonify({'status':'success', 
                            'message':'Check-in done',
                            'completed': progress["completed"],
                            'goal': habit.habit_goal,
                            'unit': habit.habit_unit
                            }), 200
        else:
            return jsonify({'status':'error', 'message':'Something went wrong'}), 400

def check_progress(habit_id):
    '''Verify progress of an existing record'''

    habit = Habit.query.filter_by(id=habit_id).first()
    if habit is None:
        return None
    # calculate range
    date = datetime.now()
    if habit.habit_frequency == 1:
        start_date = date
        end_date = date
    elif habit.habit_frequency == 2:
        start_week = date - timedelta(days=date.weekday())
        start_date = start_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_week = start_week + timedelta(days=6)
        end_date = end_week.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif habit.habit_frequency == 3:
        start_date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day = calendar.monthrange(date.year, date.month)[1]
        end_date = date.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
    else:
        return None
    habit_records = HabitRecord.query.filter(
        HabitRecord.record_date >= start_date,
        HabitRecord.record_date <= end_date
        ).all()
    completed = len(habit_records)
    return {
        "completed": completed,
        "habit_goal": habit.habit_goal,
        "status": "Completed" if completed > habit.habit_goal else "Incomplete"
    }

@app.route('/api/add_habit', methods=['POST'])
@login_required
def add_habit():
    '''add or update a habit'''
    habit_form = HabitForm()
    if request.method == 'POST':
        if habit_form.validate_on_submit():
            habit = Habit(user_id=current_user.get_id(),
                        habit_name = habit_form.habitName.data,
                        start_date = habit_form.startDate.data,
                        habit_goal = habit_form.habitGoal.data,
                        habit_unit = habit_form.habitUnit.data,
                        habit_frequency = habit_form.habitFrequency.data,
                        habit_type = habit_form.habitType.data,
                        )
            db.session.add(habit)
            db.session.commit()
            return jsonify(habit.to_dict()), 201
        else:
            return jsonify({'status':'error', 'message':'form data invalid'}), 400
    


@app.route('/api/add_challenge_habit', methods=['POST'])
@login_required
def add_challenge_habit():
    '''Add a challenge as a habit'''
    form = ChallengeToHabitForm()
    if form.validate_on_submit():
        challenge = Challenge.query.filter_by(id=form.challenge_id.data).first()
        if not challenge:
            return "Invalid challenge"
        habit = Habit.query.filter_by(id=challenge.base_habit).first()
        if not habit:
            db.session.delete(challenge)
            db.session.commit()
            return "Habit does not exist, challenge removed"
        new_habit = Habit(user_id=current_user.get_id(),
                          habit_name = habit.habit_name,
                      start_date = form.start_date.data,
                      habit_goal = habit.habit_goal,
                      habit_unit = habit.habit_unit,
                      habit_frequency = habit.habit_frequency,
                      habit_type = habit.public,
                      public = habit.start_date
                      )
        db.session.add(new_habit)
        db.session.commit()
        user_challenge = UserChallenge(
            user_id = current_user.get_id(),
            challenge_id = challenge.id,
            habit_id = new_habit.id
        )
        db.session.add(user_challenge)
        db.session.commit()
        return redirect(url_for("dashboard"))
        

@app.route('/api/challenges', methods=['GET'])
@login_required
def get_challenges():
    """Retrieve all challenges"""
    challenges = Challenge.query.all()
    result = []
    for challenge in challenges:
        result.append(challenge.to_dic())
    return jsonify(result)

@app.route('/api/add_challenge', methods=['POST'])
@login_required
def add_challenge():
    challenge_form = ChallengeForm()
    if challenge_form.validate_on_submit():

        challenge = Challenge(challenge_name = challenge_form.challenge_name.data,
                              description = challenge_form.description.data,
                              creator=current_user.get_id(),
                              base_habit = challenge_form.base_habit.data)
        db.session.add(challenge)
        db.session.commit()
        return redirect(url_for("dashboard"))

@app.route('/api/follow/<int:user_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def follow_unfollow_user(user_id):
    form = CSRFForm()
    if form.validate_on_submit():
        user_to_follow = User.query.filter_by(uid=user_id).first()
        if not user_to_follow:
            return "Error: user does not exist"
        
        if request.method == 'GET':
            return True if Follow.query.filter_by(follower_id=current_user.get_id(),
                                                  followed_id=user_to_follow.get_id()).first() else False

        if request.method == "POST":
            follow = Follow(follower_id=current_user.get_id(),
                            followed_id=user_to_follow.get_id(),
                            create_date=datetime.now())
            db.session.add(follow)
            db.session.commit()
            return redirect(url_for("dashboard"))
        if request.method == "DELETE":
            follow = Follow.query.filter_by(follower_id=current_user.get_id(),
                                   followed_id=user_to_follow.get_id()).first()
            if follow:
                db.session.delete(follow)
                db.session.commit()
            return "Success"
    else:
        return "Error: CSRF token not validated"


@app.route('/api/users', methods=['GET'])
@login_required
def get_users():
    ''' Get list of all users '''
    users = User.query.filter_by(public=True).all()
    users_list = [repr(user) for user in users]
    print(users_list)
    return jsonify(users_list)


@app.route('/api/comments', methods=['GET'])
@login_required
def get_comments():
    ''' Return all comments available for current user'''
    comments = Comment.query.filter_by(receiver_id=current_user.get_id())
    result = []
    for comment in comments:
        result.append({
            'sender_id': comment.sender_id,
            'sender_username': User.query.filter_by(uid=comment.sender_id).first().username,
            'content': comment.content,
            'public': comment.public
        })
    return jsonify(result)

@app.route('/api/tips', methods=['GET'])
def get_tips():
    ''' Return all tips shared on the website'''
    tips = Tip.query.all()
    result = []
    for tip in tips:
        result.append({
            'user_id': tip.user_id,
            'user_name': User.query.filter_by(uid=tip.user_id).first().username,
            'content': tip.content,
            'public': tip.public
        })
    return jsonify(result)