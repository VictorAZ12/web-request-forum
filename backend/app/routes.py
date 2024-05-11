from flask import redirect, url_for
from app import app, db
from app.models import User, Authentication


@app.route('/')
def index():
    return "Welcome to web app homepage!"
