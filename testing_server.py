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
        """Test that homepage version if user is not logged in renders"""
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Welcome!', result.data)


    def test_sign_up_page(self):
        """Test that sign up page renders."""

        result = self.client.get('/sign-up')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Whats your email?', result.data)


    def test_login_page(self):
        """Test that login page renders."""

        result = self.client.get('/log-in')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'''Don't have an account''', result.data)


    def test_interests_page_before_login(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)


    def test_show_recommended_books_before_user_logged_in(self):
        result = self.client.get('/recommended-books',
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Please log in.', result.data)

class BookAppTestsDatabase(unittest.TestCase):
    """Flask test that use the database"""

    def setUp(self):
        """Do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()
        app.config['SECRET_KEY'] = 'key'

        with self.client as c:
            with c.session_transaction() as session:
                session['user_id'] = 1

        # Connect to test database
        model.connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        model.db.create_all()
        test_data()


    def tearDown(self):
        """Do after each test"""

        model.db.session.close()
        model.db.drop_all()

    def test_user_created_in_db(self):
        """Test that user was successfully created in db."""

        user = model.User.query.get(1)

        self.assertEqual('user1@test.com', user.email)
        self.assertEqual('test', user.password)


    def test_unsuccessful_sign_up_because_passwords_do_not_matcg(self):
        """Test that sign up when password does not match confirmed password"""

        result = self.client.post('/handle-sign-up',
                                 data= {'email': 'sign_up_test@test.com',
                                 'password': 'test',
                                 'confirm-password': 'test1',
                                 'profile-name': 'Jane Doe',
                                 'birth-month': 'july',
                                 'birth-day': '14',
                                 'birth-year': '1998',
                                 'gender': 'Female'},
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Passwords do not match.', result.data)


    def test_successful_sign_up(self):
        """Test that sign up successfully creates user in db"""

        result = self.client.post('/handle-sign-up',
                                 data= {'email': 'sign_up_test@test.com',
                                 'password': 'test',
                                 'confirm-password': 'test',
                                 'profile-name': 'Jane Doe',
                                 'birth-month': 'july',
                                 'birth-day': '14',
                                 'birth-year': '1998',
                                 'gender': 'Female'},
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Account created! Please sign in.', result.data)
        self.assertIn(b'''Don't have an account''', result.data)


    def test_sign_up_when_account_already_exists(self):
        """Test that sign up when account already exists"""

        result = self.client.post('/handle-sign-up',
                                 data= {'email': 'user1@test.com',
                                 'password': 'test',
                                 'confirm-password': 'test',
                                 'profile-name': 'Jane Doe',
                                 'birth-month': 'july',
                                 'birth-day': '14',
                                 'birth-year': '1998',
                                 'gender': 'Female'},
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Account already exists.', result.data)


    def test_successful_first_time_login(self):

        result = self.client.post('/log-in-credentials',
                                data= {'email':'user1@test.com',
                                      'password':'test'},
                                       follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<input type="checkbox" name="interests" value="young adult nonfiction">', result.data)


    def test_successful_login_for_user_who_has_logged_in_at_once(self):
        result = self.client.post('/log-in-credentials',
                                data={'email': 'user2@test.com',
                                      'password': 'test'},
                                       follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Your Library', result.data)


    def test_unsuccessful_login(self):
        result = self.client.post('/log-in-credentials',
                                 data={'email': 'not_a_user@test.com',
                                       'password': 'test'},
                                       follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'The email and password you entered did not match our records.', result.data)


    def test_interest_page_after_login(self):
        result = self.client.get('/interests')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Art', result.data)


    def test_setting_interest(self):
        result = self.client.post('/handle-user-interests',
                                  data={'interests':'art'},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Your Library', result.data)

        interest = model.UserInterest.query.get((1,1))
        self.assertEqual('art', interest.interest.interest)


if __name__ == '__main__':
    unittest.main()