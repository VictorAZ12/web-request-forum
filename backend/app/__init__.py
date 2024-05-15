from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config
import os
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Import models and create tables
from app import models
with app.app_context():
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if not os.path.exists(db_path):
        db.create_all()
        print("Database created successfully.")
    else:
        print("Database already exists.")

# Create Login
login_manager = LoginManager(app)
# Register user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

from app import routes
