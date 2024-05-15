from datetime import datetime
from app import db, bcrypt
from flask_login import UserMixin



class User(db.Model, UserMixin):

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(100))
    dob = db.Column(db.Date)
    address = db.Column(db.String(200))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    public = db.Column(db.Boolean, default=True)
    # Authentication attributes
    # is_active, is_authenticated,  get_id() provided by UserMixin
    hashed_password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return f"User('{self.uid}', '{self.username}')"
    def to_dict(self):
        return {
            'uid': self.uid,
            'fullname': self.fullname,
            'dob': self.dob.strftime('%Y-%m-%d') if self.dob else None,
            'address': self.address,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,
            'create_date': self.create_date.strftime('%Y-%m-%d %H:%M:%S') if self.create_date else None,
            'public': self.public
        }
    def get_id(self):
        return str(self.id)
    def __eq__(self, other):
        """
        Checks the equality of two `UserMixin` objects using `get_id`.
        """
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()

    def __ne__(self, other):
        """
        Checks the inequality of two `UserMixin` objects using `get_id`.
        """
        equal = self.__eq__(other)
        return not equal





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
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'creator_id': self.creator_id,
            'public': self.public
        }

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
