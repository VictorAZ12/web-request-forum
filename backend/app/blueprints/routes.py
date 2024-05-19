from flask import redirect, url_for, request, jsonify, flash, render_template
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta
import calendar

from app import db, bcrypt
from app.models import User, UserChallenge, Challenge, Habit, HabitType, Follow, Comment, Tip, HabitRecord
from app.blueprints.main import main
from app.forms import LoginForm, RegisterForm, HabitForm, ChallengeForm, CSRFForm

# Pages
@main.route('/')
@login_required
def home():
    """Returns homepage html"""
    flash("Welcome to web app homepage!")
    return "Welcome to web app homepage!"

@main.route('/register', methods=['POST'])
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
            return jsonify({'status':'error', 'message':'Username occupied.'}), 400
        # create a new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, username=username, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user) # login user
        return jsonify({'status':'success', 'message':'Account registered successfully.'}), 201
    else:
        return jsonify({'status':'error', 'message':'Form data invalid'}), 400

@main.route('/login', methods=['POST'])
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
            return jsonify({'status':'success', 'message':'Logged in successfully'}), 200
        else:
            return jsonify({'status':'error', 'message': 'Login unsuccessful, please check email and password'}), 401
    else:
        return jsonify({'status':'error', 'message':'Form data invalid'}), 400

@main.route('/index', methods=['GET', 'POST'])
def index():
    """Index page with login and register forms"""
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template('HabitNest.html', login_form=login_form, register_form=register_form)

@main.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    habit_form = HabitForm()
    challenge_form = ChallengeForm()
    return render_template('Dashboard.html', 
                           habit_form=habit_form,
                           challenge_form=challenge_form,
                           user=current_user)

@main.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')

# APIs
@main.route('/api/habit_types', methods=['GET'])
@login_required
def get_habit_types():
    """Retrieve all habit types"""
    habit_types = HabitType.query.all()
    result = [habit_type.to_dic() for habit_type in habit_types]
    return jsonify(result)

@main.route('/api/habits', defaults={'habit_id': None}, methods=['GET'])
@main.route('/api/habits/<int:habit_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_habits(habit_id):
    """Retrieve all habits of current user or a specific habit"""
    user_id = current_user.get_id()
    if request.method == 'GET':
        if habit_id is None:
            user_habits = Habit.query.filter_by(user_id=user_id).all()
            result = []
            for habit in user_habits:
                user_challenge = UserChallenge.query.filter_by(habit_id=habit.id).first()
                habit_dic = habit.to_dict()
                habit_dic["is_challenge"] = False if user_challenge is None else True
                result.append(habit_dic)
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
        if habit:
            try:
                db.session.delete(habit)
                db.session.commit()
                return jsonify({'status':'success', 'message':'Habit deleted.'}), 200
            except:
                return jsonify({'status':'error', 'message':'Something is wrong.'}), 500
        else:
            return jsonify({'status':'error', 'message':'Habit not found'}), 404

@main.route('/api/habits/checkin/<int:habit_id>', methods=['GET', 'POST'])
def check_in(habit_id):
    if request.method == 'GET':
        habit_records = HabitRecord.query.filter_by(habit=habit_id).all()
        result = [str(habit_record.record_date) for habit_record in habit_records]
        return jsonify(result), 200
    if request.method == 'POST':
        habit = Habit.query.filter_by(id=habit_id).first()
        if habit is None:
            return jsonify({'status':'error', 'message':'Habit not found'}), 404
        user_id = current_user.get_id()
        if str(habit.user_id) != str(user_id):
            return jsonify({'status':'error', 'message':'Not your habit'}), 404
        record_date = datetime.now()
        habit_record = HabitRecord(record_date=record_date, habit=habit_id)
        db.session.add(habit_record)
        db.session.commit()
        progress = check_progress(habit_id)
        if progress:
            return jsonify({'status':'success', 
                            'message':'Check-in done',
                            'completed': progress["completed"],
                            'goal': habit.habit_goal,
                            'unit': habit.habit_unit
                            }), 200
        else:
            return jsonify({'status':'error', 'message':'Something went wrong'}), 400

@main.route('/api/habits/progress/<int:habit_id>', methods=['GET'])
@login_required
def view_progress(habit_id):
    if request.method == 'GET':
        habit = Habit.query.filter_by(id=habit_id).first()
        if habit is None:
            return jsonify({'status':'error', 'message':'Habit not found'}), 404
        if str(current_user.get_id()) != str(habit.user_id):
            return jsonify({'status':'error', 'message':'Not your habit'}), 401
        progress = check_progress(habit_id)
        if progress:
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
    date = datetime.now()
    if habit.habit_frequency == 1:
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = date.replace(hour=23, minute=59, second=59, microsecond=999999)
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
        HabitRecord.habit == habit_id,
        HabitRecord.record_date >= start_date,
        HabitRecord.record_date <= end_date
        ).all()
    completed = len(habit_records)
    return {
        "completed": completed,
        "habit_goal": habit.habit_goal,
        "status": "Completed" if completed >= habit.habit_goal else "Incomplete"
    }

@main.route('/api/add_habit', methods=['POST'])
@login_required
def add_habit():
    '''Add or update a habit'''
    habit_form = HabitForm()
    if request.method == 'POST':
        if habit_form.validate_on_submit():
            habit = Habit(user_id=current_user.get_id(),
                          habit_name=habit_form.habitName.data,
                          start_date=habit_form.startDate.data,
                          habit_goal=habit_form.habitGoal.data,
                          habit_unit=habit_form.habitUnit.data,
                          habit_frequency=habit_form.habitFrequency.data,
                          habit_type=habit_form.habitType.data,
                          )
            db.session.add(habit)
            db.session.commit()
            return jsonify(habit.to_dict()), 201
        else:
            return jsonify({'status':'error', 'message':'Form data invalid'}), 400

@main.route('/api/challenge_habit/progress/<int:habit_id>', methods=['GET'])
@login_required
def challenge_habit_progress(habit_id):
    challenge_habit = UserChallenge.query.filter_by(habit_id=habit_id).first()
    on_track = "On track" if check_progress(habit_id)["status"] == "Completed" else "Off track"
    if challenge_habit:
        challenge_habits_all = UserChallenge.query.filter_by(challenge_id=challenge_habit.challenge_id).all()
        total, completed = 0, 0
        for habit in challenge_habits_all:
            result = check_progress(habit.habit_id)
            if result["status"] == "Completed":
                completed += 1
            total += 1
        return jsonify({'status':'success', 
                        'total': total,
                        'completed': completed,
                        'status': on_track}), 200
    else:
        return jsonify({'status':'error', 'message':'Habit not found'}), 404

@main.route('/api/add_challenge_habit/<int:challenge_id>', methods=['POST'])
@login_required
def add_challenge_habit(challenge_id):
    '''Add a challenge as a habit'''
    habit_form = HabitForm()
    if request.method == 'POST':
        if habit_form.validate_on_submit():
            habit = Habit(user_id=current_user.get_id(),
                          habit_name=habit_form.habitName.data,
                          start_date=habit_form.startDate.data,
                          habit_goal=habit_form.habitGoal.data,
                          habit_unit=habit_form.habitUnit.data,
                          habit_frequency=habit_form.habitFrequency.data,
                          habit_type=habit_form.habitType.data,
                          )
            db.session.add(habit)
            db.session.commit()
            user_challenge = UserChallenge(user_id=current_user.get_id(),
                                           challenge_id=challenge_id,
                                           habit_id=habit.id)
            db.session.add(user_challenge)
            db.session.commit()
            habit_dic = habit.to_dict()
            habit_dic["is_challenge"] = True
            return jsonify(habit_dic), 201
        else:
            return jsonify({'status':'error', 'message':'Form data invalid'}), 400

@main.route('/api/challenges', methods=['GET'])
@login_required
def get_challenges():
    """Retrieve all challenges"""
    challenges = Challenge.query.all()
    result = [challenge.to_dic() for challenge in challenges]
    return jsonify(result)

@main.route('/api/add_challenge', methods=['POST'])
@login_required
def add_challenge():
    challenge_form = ChallengeForm()
    if challenge_form.validate_on_submit():
        challenge = Challenge(challenge_name=challenge_form.challengeName.data,
                              description=challenge_form.description.data,
                              creator_id=current_user.get_id(),
                              challenge_goal=challenge_form.challengeGoal.data,
                              challenge_unit=challenge_form.challengeUnit.data,
                              challenge_frequency=challenge_form.challengeFrequency.data,
                              challenge_type=challenge_form.challengeType.data)
        db.session.add(challenge)
        db.session.commit()
        return jsonify(challenge.to_dic()), 200
    else:
        return jsonify({'status':'error', 'message':'Form data invalid'}), 400

@main.route('/api/follow/<int:user_id>', methods=['GET', 'POST', 'DELETE'])
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
            return redirect(url_for("main.dashboard"))
        if request.method == "DELETE":
            follow = Follow.query.filter_by(follower_id=current_user.get_id(),
                                   followed_id=user_to_follow.get_id()).first()
            if follow:
                db.session.delete(follow)
                db.session.commit()
            return "Success"
    else:
        return "Error: CSRF token not validated"

@main.route('/api/users', methods=['GET'])
@login_required
def get_users():
    ''' Get list of all users '''
    users = User.query.filter_by(public=True).all()
    users_list = [repr(user) for user in users]
    return jsonify(users_list)

@main.route('/api/comments', methods=['GET'])
@login_required
def get_comments():
    ''' Return all comments available for current user'''
    comments = Comment.query.filter_by(receiver_id=current_user.get_id())
    result = [{'sender_id': comment.sender_id,
               'sender_username': User.query.filter_by(uid=comment.sender_id).first().username,
               'content': comment.content,
               'public': comment.public} for comment in comments]
    return jsonify(result)

@main.route('/api/tips', methods=['GET'])
def get_tips():
    ''' Return all tips shared on the website'''
    tips = Tip.query.all()
    result = [{'user_id': tip.user_id,
               'user_name': User.query.filter_by(uid=tip.user_id).first().username,
               'content': tip.content,
               'public': tip.public} for tip in tips]
    return jsonify(result)
