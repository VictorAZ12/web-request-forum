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
    challengeName = StringField('Challenge name', validators=[DataRequired()])
    description = StringField('Description')
    challengeGoal = IntegerField('Goal numbers', validators=[DataRequired()])
    challengeUnit = StringField('Unit', validators=[DataRequired()])
    challengeFrequency = IntegerField('Frequency', validators=[DataRequired(), NumberRange(1,3)])
    challengeType = IntegerField('Type', validators=[DataRequired()])
    submit = SubmitField('Create challenge')


class CommentForm(FlaskForm):
    content = StringField('Content')
    submit = SubmitField('Share tip')

class TipForm(FlaskForm):
    content = StringField('Content')
    submit = SubmitField('Share tip')

class CSRFForm(FlaskForm):
    """For CSRF protection only"""
    pass