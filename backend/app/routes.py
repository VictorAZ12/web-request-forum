from flask import redirect, url_for, request, jsonify, flash, render_template
from app import app, db, bcrypt
from app.models import User, UserChallenge, Challenge
from flask_login import login_user, current_user, logout_user, login_required
# Pages
@app.route('/')
def index():
    """Returns homepage html"""
    flash("Welcome to web app homepage!")
    return "Welcome to web app homepage!"

# Test only login protected page
@app.route('/protected')
@login_required
def protected():
    return "You're logged in and can access this protected page"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # check existence
        existing_email_user = User.query.filter_by(email=email).first()
        existing_username_user = User.query.filter_by(username=username).first()
        if existing_email_user:
            flash('Email is already registered. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        if existing_username_user:
            flash('Username is already registered. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

# APIs

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
