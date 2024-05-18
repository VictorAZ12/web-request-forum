from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, UserChallenge, Challenge
from app.forms import LoginForm, RegisterForm
from app.blueprints.main import main
from app import db, bcrypt

@main.route('/')
@login_required
def home():
    """Returns homepage html"""
    flash("Welcome to web app homepage!")
    return "Welcome to web app homepage!"

@main.route('/protected')
@login_required
def protected():
    return "You're logged in and can access this protected page"

@main.route('/register', methods=['POST'])
def register():
    """Register route"""
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        username = register_form.username.data
        password = register_form.password.data
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

@main.route('/login', methods=['POST'])
def login():
    """Login route"""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.hashed_password, password):
            login_user(user)
            return redirect(url_for('main.protected'))
        else:
            return 'Login Unsuccessful. Please check email and password'

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

@main.route('/api/users', methods=['GET'])
def get_users():
    ''' Get list of all users '''
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)

@main.route('/api/user_challenge/', methods=['GET'])
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
