"""Test functions in server.py"""
import unittest

from server import app
import model
from test_data import test_data


class BookAppTests(unittest.TestCase):
    """Testing intergration of Flask server"""

    def setUp(self):
        """Do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage_before_login(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Welcome!', result.data)


    def test_sign_up_page(self):
        result = self.client.get('/sign-up')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Whats your email?', result.data)


    def test_login_page(self):
        result = self.client.get('/log-in')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'''Don't have an account''', result.data)



class BookAppTestsDatabase(unittest.TestCase):
    """Flask test that use the database"""

    def setUp(self):
        """Do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        model.connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        model.db.create_all()
        test_data()

    def tearDown(self):
        """Do after each test"""

        model.db.session.close()
        model.db.drop_all()

    def test_homepage_after_login(self):
        result = self.client.get('/log-in-credentials',
                                data={'email': 'user1@test.com',
                                      'password': 'test'},
                                       follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Your Library', result.data)


if __name__ == '__main__':
    unittest.main()