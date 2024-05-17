from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class HabitForm(FlaskForm):
    habit_name = StringField('Habit name', validators=[DataRequired()])
    start_date = DateField('Target date', validators=[DataRequired()])
    habit_goal = IntegerField('Goal numbers', validators=[DataRequired()])
    habit_unit = StringField('Unit', validators=[DataRequired()])
    habit_frequency = IntegerField('Frequency', validators=[DataRequired(), NumberRange(1,3)])
    habit_type = IntegerField('Habit', validators=[DataRequired()])
    public = BooleanField('Publicly Visible', validators=[DataRequired])
    submit = SubmitField('Add habit')

class ChallengeForm(FlaskForm):
    challenge_name = StringField('Challenge name', validators=[DataRequired()])
    content = StringField('Content')
    base_habit = IntegerField('Base_habit', validators=[DataRequired()])
    submit = SubmitField('Create challenge')

class FollowForm(FlaskForm):
    """For CSRF protection only"""
    pass