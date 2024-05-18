import unittest
import os
import sys

# Ensure the app module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from config import Config

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Config)
        self.client = self.app.test_client()

    def test_index_page(self):
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to HabitNest', response.data)

if __name__ == '__main__':
    unittest.main()
