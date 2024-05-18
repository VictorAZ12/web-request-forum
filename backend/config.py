import os

# Config file
# Source: https://flask.palletsprojects.com/en/2.3.x/config/#configuring-from-python-files

class Config(object):
    """Maintains flask app configs"""
    SECRET_KEY = '12345678'  # Test purpose only
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'webapp.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False
