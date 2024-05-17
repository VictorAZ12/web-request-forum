from datetime import datetime
from app import db, bcrypt
from flask_login import UserMixin



class User(db.Model, UserMixin):

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(100))
    dob = db.Column(db.Date)
    # address = db.Column(db.String(200))
    # last_login = db.Column(db.DateTime, default=datetime.utcnow)
    # create_date = db.Column(db.DateTime, default=datetime.utcnow)
    public = db.Column(db.Boolean, default=True)
    # Authentication attributes
    # is_active, is_authenticated,  get_id() provided by UserMixin
    hashed_password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return f"User('{self.uid}', '{self.username}')"

    def get_id(self):
        """Overwrite get_id in UserMixin"""
        return str(self.uid)
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

class HabitType(db.Model):
    __tablename__ = 'habit_type'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    habit_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    habit_goal = db.Column(db.Integer, nullable=False) 
    habit_unit = db.Column(db.String(100), nullable=False)
    habit_frequency = db.Column(db.Integer, nullable=False) # 1 for per day, 2 for per week, 3 for per month
    habit_type = db.Column(db.Integer, db.ForeignKey('habit_type.id'))
    public = db.Column(db.Boolean, default=True)
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'habit_name': self.habit_name,
            'start_date': self.start_date.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.start_date, datetime) else self.start_date,
            'habit_goal': self.habit_goal,
            'habit_unit': self.habit_unit,
            'habit_frequency': self.habit_frequency,
            'habit_type': self.habit_type,
            'public': self.public
        }


class HabitRecord(db.Model):
    __tablename__ = 'habit_record'
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.DateTime, default=datetime.utcnow)
    habit = db.Column(db.Integer, db.ForeignKey('habit.id'))

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenge_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    creator = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    base_habit = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    def to_dic(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'description': self.description,
            'creator': self.user_id,
            'base_habit': self.base_habit
        }

class UserChallenge(db.Model):
    __tablename__ = 'user_challenge'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
