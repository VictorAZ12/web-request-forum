from flask import redirect, url_for, request, jsonify
from app import app, db
from app.models import User, Authentication
from app.models import User, Authentication, Follow, Comment, Tip, Habit, Goal, Challenge, UserChallenge, ChallengeGoal, UserGoal
# Pages
@app.route('/')
def index():
    """Returns homepage html"""
    return "Welcome to web app homepage!"
