from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    # Register the user_loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not os.path.exists(db_path):
            db.create_all()
            print("Database created successfully.")
        else:
            print("Database already exists.")

    return app
