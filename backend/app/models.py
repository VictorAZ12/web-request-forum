from datetime import datetime
from app import db, bcrypt

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date)
    address = db.Column(db.String(200))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    public = db.Column(db.Boolean, default=True)
    def __repr__(self):
        return f"User('{self.uid}', '{self.fullname}')"

class Authentication(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    expiry_date = db.Column(db.DateTime, default=datetime.utcnow)
    expired = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    public = db.Column(db.Boolean, default=True)

class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    public = db.Column(db.Boolean, default=True)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    habit_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    target_date = db.Column(db.DateTime)
    progress = db.Column(db.Float)
    public = db.Column(db.Boolean, default=True)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    public = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    public = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)

class UserChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    target_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    public = db.Column(db.Boolean, default=True)

class ChallengeGoal(db.Model):
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), primary_key=True)

class UserGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    target_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    public = db.Column(db.Boolean, default=True)
