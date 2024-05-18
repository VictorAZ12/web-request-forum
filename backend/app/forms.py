from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class HabitForm(FlaskForm):
    habitName = StringField('Habit name', validators=[DataRequired()])
    startDate = DateField('Start date', validators=[DataRequired()])
    habitGoal = IntegerField('Goal numbers', validators=[DataRequired()])
    habitUnit = StringField('Unit', validators=[DataRequired()])
    habitFrequency = IntegerField('Frequency', validators=[DataRequired(), NumberRange(1,3)])
    habitType = IntegerField('Habit', validators=[DataRequired()])
    submit = SubmitField('Add habit')

class ChallengeForm(FlaskForm):
    challenge_name = StringField('Challenge name', validators=[DataRequired()])
    content = StringField('Content')
    base_habit = IntegerField('Base_habit', validators=[DataRequired()])
    submit = SubmitField('Create challenge')

class ChallengeToHabitForm(FlaskForm):
    challenge_id = IntegerField('Challenge', validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    submit = SubmitField('Enrol in challenge')

class CommentForm(FlaskForm):
    content = StringField('Content')
    submit = SubmitField('Share tip')

class TipForm(FlaskForm):
    content = StringField('Content')
    submit = SubmitField('Share tip')

class CSRFForm(FlaskForm):
    """For CSRF protection only"""
    pass