from flask import redirect, url_for, request, jsonify
from app import app, db
# Pages
@app.route('/')
def index():
    """Returns homepage html"""
    return "Welcome to web app homepage!"
