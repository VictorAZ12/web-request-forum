import unittest
import os
import sys
from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Ensure the app module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db, bcrypt
from app.models import User
from app.forms import LoginForm, RegisterForm
from config import Config


class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test config with a test database
        self.app = create_app(Config)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['LOGIN_DISABLED'] = True  # Disable login for the test
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Welcome to web app homepage!", response.data)

    def test_register(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                email='test@example.com',
                username='testuser',
                password='password123'
            ))
            self.assertEqual(response.status_code, 201)

    def test_login(self):
        with self.client:
            # First, register a new user
            response = self.client.post('/register', data=dict(
                email='logintest@example.com',
                username='logintestuser',
                password='password123'
            ))
            self.assertEqual(response.status_code, 201)

            # Then, attempt to log in with the registered user's credentials
            response = self.client.post('/login', data=dict(
                email='logintest@example.com',
                password='password123'
            ))
            self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        with self.client:
            response = self.client.get('/dashboard')
            self.assertEqual(response.status_code, 200)





if __name__ == '__main__':
    unittest.main()

