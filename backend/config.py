import os
# Config file
# Source: https://flask.palletsprojects.com/en/2.3.x/config/#configuring-from-python-files

class Config(object):
    """Maintains flask app configs"""
    SECRET_KEY = '12345678' # Test purpose only
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'webapp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
