from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired

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
    description = StringField('Description', default="")
    target_date = DateField('Target date', validators=[DataRequired()])
    submit = SubmitField('Add habit')

class ChallengeForm(FlaskForm):
    challenge_name = StringField('Challenge name', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    public = BooleanField('Public?')
    submit = SubmitField('Create challenge')
