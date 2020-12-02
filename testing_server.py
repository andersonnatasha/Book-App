"""Test functions in server.py"""
import unittest

from server import app
import model
from test_data import test_data
from datetime import datetime


class BookAppTests(unittest.TestCase):
    """Testing intergration of Flask server"""

    def setUp(self):
        """Do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage_before_login(self):
        """Test that homepage version if user is not logged in renders"""
        result = self.client.get('/')
        self.assertEqual(200, result.status_code)
        self.assertIn(b'Welcome!', result.data)


    def test_sign_up_page(self):
        """Test that sign up page renders."""

        result = self.client.get('/sign-up')
        self.assertEqual(200, result.status_code)
        self.assertIn(b'Whats your email?', result.data)


    def test_login_page(self):
        """Test that login page renders."""

        result = self.client.get('/log-in')
        self.assertEqual(200, result.status_code)
        self.assertIn(b'''Don't have an account''', result.data)


    # def test_interests_page_before_login(self):
    #     result = self.client.get('/')
    #     self.assertEqual(200, result.status_code)


    # def test_recommended_books_page_before_user_logged_in(self):
    #     result = self.client.get('/recommended-books',
    #                              follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Please log in to see your recommended books.', result.data)


    # def test_read_books_page_before_user_logged_in(self):
    #     result = self.client.get('/read-books',
    #                              follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Please log in to see your read books.', result.data)


    # def test_liked_books_page_before_user_logged_in(self):
    #     result = self.client.get('/liked-books',
    #                              follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Please log in to see your liked books.', result.data)


    # def test_to_be_read_books_page_before_user_logged_in(self):
    #     result = self.client.get('/to-be-read-books',
    #                              follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Please log in to see your tbr list.', result.data)


    # def test_search_a_book_page_before_user_logged_in(self):
    #     result = self.client.get('/search-a-book',
    #                              follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Please log in.', result.data)


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


    # def test_book1_created_in_db(self):

    #     book1 = model.Book.query.get(1)

    #     self.assertEqual('Test Title1', book1.title)
    #     self.assertEqual(1, book1.book_id)

    # def test_author1_created_in_db(self):

    #     author1 = model.Author.query.get(1)

    #     self.assertEqual('Octavia Thomas', author1.full_name)
    #     self.assertEqual(1, author1.author_id)
    #     self.assertEqual(1, author1.book_id)

    # def test_bookauthor1_created_in_db(self):

    #     bookauthor1 = model.BookAuthor.query.get((1,1))

    #     self.assertEqual(1, bookauthor1.book_id)
    #     self.assertEqual(1, bookauthor1.author_id)
    #     self.assertEqual('Octavia Thomas', bookauthor1.author.full_name)
    #     self.assertEqual('Test Title1', bookauthor1.book.title)

    # def test_read_book_in_library_created_in_db(self):

    #     read_book_in_library = model.BookInLibrary.query.get((1,1))

    #     self.assertEqual(1, read_book_in_library.book_id)
    #     self.assertEqual(1, read_book_in_library.user_id)
    #     self.assertEqual(True, read_book_in_library.read)
    #     self.assertEqual(datetime, type(read_book_in_library.read_date))
    #     self.assertEqual(False, read_book_in_library.liked)
    #     self.assertEqual(None, read_book_in_library.liked_date)
    #     self.assertEqual(False, read_book_in_library.to_be_read)
    #     self.assertEqual(None, read_book_in_library.to_be_read_date)

    # def test_liked_book_in_library_created_in_db(self):

    #     liked_book_in_library = model.BookInLibrary.query.get((2,1))

    #     self.assertEqual(2, liked_book_in_library.book_id)
    #     self.assertEqual(1, liked_book_in_library.user_id)
    #     self.assertEqual(True, liked_book_in_library.read)
    #     self.assertEqual(datetime, type(liked_book_in_library.read_date))
    #     self.assertEqual(True, liked_book_in_library.liked)
    #     self.assertEqual(datetime, type(liked_book_in_library.liked_date))
    #     self.assertEqual(False, liked_book_in_library.to_be_read)
    #     self.assertEqual(None, liked_book_in_library.to_be_read_date)

    # def test_tbr_book_in_library_created_in_db(self):

    #     tbr_book_in_library = model.BookInLibrary.query.get((3,1))

    #     self.assertEqual(3, tbr_book_in_library.book_id)
    #     self.assertEqual(1, tbr_book_in_library.user_id)
    #     self.assertEqual(False, tbr_book_in_library.read)
    #     self.assertEqual(None, tbr_book_in_library.read_date)
    #     self.assertEqual(False, tbr_book_in_library.liked)
    #     self.assertEqual(None, tbr_book_in_library.liked_date)
    #     self.assertEqual(True, tbr_book_in_library.to_be_read)
    #     self.assertEqual(datetime, type(tbr_book_in_library.to_be_read_date))


    # def test_bookshelf_created_in_db(self):

    #     bookshelf = model.Bookshelf.query.get(1)

    #     self.assertEqual(1, bookshelf.user_id)
    #     self.assertEqual('Magical Realism', bookshelf.name)


    # def test_book_on_bookshelf_added_to_db(self):

    #     book_on_bookshelf = model.BookOnBookshelf.query.get(1)

    #     self.assertEqual('Test Title1', book_on_bookshelf.book.title)
    #     self.assertEqual(datetime, type(book_on_bookshelf.date_added))


    # def test_unsuccessful_sign_up_because_passwords_do_not_match(self):
    #     """Test that sign up when password does not match confirmed password"""

    #     result = self.client.post('/handle-sign-up',
    #                              data= {'email': 'sign_up_test@test.com',
    #                              'password': 'test',
    #                              'confirm-password': 'test1',
    #                              'profile-name': 'Jane Doe',
    #                              'birth-month': 'july',
    #                              'birth-day': '14',
    #                              'birth-year': '1998',
    #                              'gender': 'Female'},
    #                              follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Passwords do not match.', result.data)


    # def test_successful_sign_up(self):
    #     """Test that sign up successfully creates user in db"""

    #     result = self.client.post('/handle-sign-up',
    #                              data= {'email': 'sign_up_test@test.com',
    #                              'password': 'test',
    #                              'confirm-password': 'test',
    #                              'profile-name': 'Jane Doe',
    #                              'birth-month': 'july',
    #                              'birth-day': '14',
    #                              'birth-year': '1998',
    #                              'gender': 'Female'},
    #                              follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Account created! Please sign in.', result.data)
    #     self.assertIn(b'''Don't have an account''', result.data)


    # def test_sign_up_when_account_already_exists(self):
    #     """Test that sign up when account already exists"""

    #     result = self.client.post('/handle-sign-up',
    #                              data= {'email': 'user1@test.com',
    #                              'password': 'test',
    #                              'confirm-password': 'test',
    #                              'profile-name': 'Jane Doe',
    #                              'birth-month': 'july',
    #                              'birth-day': '14',
    #                              'birth-year': '1998',
    #                              'gender': 'Female'},
    #                              follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Account already exists.', result.data)


    # def test_successful_first_time_login(self):

    #     result = self.client.post('/log-in-credentials',
    #                               data= {'email':'user1@test.com',
    #                                     'password':'test'},
    #                                     follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'<input type="checkbox" name="interests" value="young adult nonfiction">', result.data)


    # def test_successful_login_for_user_who_has_logged_in_at_once(self):
    #     result = self.client.post('/log-in-credentials',
    #                             data={'email': 'user2@test.com',
    #                                   'password': 'test'},
    #                                    follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Your Library', result.data)


    # def test_unsuccessful_login(self):
    #     result = self.client.post('/log-in-credentials',
    #                              data={'email': 'not_a_user@test.com',
    #                                    'password': 'test'},
    #                                    follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'The email and password you entered did not match our records.', result.data)


    # def test_interest_page_after_login(self):
    #     result = self.client.get('/interests')
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Art', result.data)


    # def test_setting_interest(self):
    #     result = self.client.post('/handle-user-interests',
    #                               data={'interests':'art'},
    #                               follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Your Library', result.data)

    #     interest = model.UserInterest.query.get((1,1))
    #     self.assertEqual('art', interest.interest.interest)


    # def test_searching_a_book(self):
    #     result = self.client.get('/search-a-book',
    #                               query_string={'search': 'Another Country'})
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Another Country', result.data)
    #     self.assertIn(b'Read', result.data)
    #     self.assertIn(b'Liked', result.data)
    #     self.assertIn(b'TBR', result.data)
    #     self.assertIn(b'Add to Bookshelf', result.data)
    #     self.assertIn(b'<img src="http://books.google', result.data)
    #     self.assertIn(b'James Baldwin', result.data)
    #     self.assertIn(b'Nominated as one of', result.data)


    # def test_view_read_books_page(self):
    #     result = self.client.get('/read-books',)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b"Your Read Books", result.data)


    # def test_view_liked_books_page(self):
    #     result = self.client.get('/liked-books',)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b"Your Liked Books", result.data)


    # def test_view_to_be_read_books_page(self):
    #     result = self.client.get('/to-be-read-books',)
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b"Your TBR List", result.data)


    # def test_view_recommended_books_page(self):
    #     result = self.client.get('/recommended-books')
    #     self.assertEqual(200, result.status_code)
    #     self.assertIn(b'Your Recommended Books', result.data)


    # def test_marking_a_new_book_in_library_as_read(self):
    #     result = self.client.post('/mark-as-read',
    #                               data={'title': 'Another Country',
    #                                     'subtitle': None,
    #                                     'authors': 'James Baldwin',
    #                                     'image_link': None,
    #                                     'categories': None,
    #                                     'description': None,
    #                                     'isbn_13': '9780804149716'})
    #     self.assertEqual(200, result.status_code)
    #     read_book = model.BookInLibrary.query.get((4,1))
    #     self.assertIn(b"Added to your read books.", result.data)
    #     self.assertEqual('Another Country', read_book.book.title)
    #     self.assertEqual(True, read_book.read)
    #     self.assertEqual(datetime, type(read_book.read_date))
    #     self.assertEqual(False, read_book.liked)
    #     self.assertEqual(None, read_book.liked_date)
    #     self.assertEqual(False, read_book.to_be_read)
    #     self.assertEqual(None, read_book.to_be_read_date)


    # def test_marking_a_new_book_in_library_as_liked(self):
    #     result = self.client.post('/mark-as-liked',
    #                               data={'title': 'Another Country',
    #                                     'subtitle': None,
    #                                     'authors': 'James Baldwin',
    #                                     'image_link': None,
    #                                     'categories': None,
    #                                     'description': None,
    #                                     'isbn_13': '9780804149716'})
    #     self.assertEqual(200, result.status_code)
    #     liked_book = model.BookInLibrary.query.get((4,1))
    #     self.assertEqual(True, liked_book.liked)
    #     self.assertEqual(datetime, type(liked_book.liked_date))
    #     self.assertEqual(True, liked_book.read)
    #     self.assertEqual(datetime, type(liked_book.read_date))
    #     self.assertEqual(False, liked_book.to_be_read)
    #     self.assertEqual(None, liked_book.to_be_read_date)

    # def test_marking_a_new_book_in_library_as_to_be_read(self):
    #     result = self.client.post('/mark-as-to-be-read',
    #                               data={'title': 'Another Country',
    #                                     'subtitle': None,
    #                                     'authors': 'James Baldwin',
    #                                     'image_link': None,
    #                                     'categories': None,
    #                                     'description': None,
    #                                     'isbn_13': '9780804149716'})
    #     self.assertEqual(200, result.status_code)
    #     to_be_read_book = model.BookInLibrary.query.get((4,1))
    #     self.assertEqual(True, to_be_read_book.to_be_read)
    #     self.assertEqual(datetime, type(to_be_read_book.to_be_read_date))
    #     self.assertEqual(False, to_be_read_book.read)
    #     self.assertEqual(None, to_be_read_book.read_date)
    #     self.assertEqual(False, to_be_read_book.liked)
    #     self.assertEqual(None, to_be_read_book.liked_date)

    # def test_changing_read_book_to_tbr_book(self):

    #     read_book_in_library = model.BookInLibrary.query.filter(model.BookInLibrary.read == True).first()
    #     result = self.client.post('/mark-as-to-be-read',
    #                               data = {'title': read_book_in_library.book.title,
    #                                       'subtitle': read_book_in_library.book.subtitle,
    #                                       'authors': read_book_in_library.book.authors,
    #                                       'image_link': read_book_in_library.book.image_link,
    #                                       'categories': read_book_in_library.book.categories,
    #                                       'description': read_book_in_library.book.description,
    #                                       'isbn_13': read_book_in_library.book.isbn_13})

    #     self.assertEqual(200, result.status_code)
    #     updated_book_in_library = model.BookInLibrary.query.get((1,1))
    #     self.assertEqual(True, updated_book_in_library.to_be_read)
    #     self.assertEqual(datetime, type(updated_book_in_library.to_be_read_date))
    #     self.assertEqual(False, updated_book_in_library.read)
    #     self.assertEqual(None, updated_book_in_library.read_date)
    #     self.assertEqual(False, updated_book_in_library.liked)
    #     self.assertEqual(None, updated_book_in_library.liked_date)

    # def test_changing_tbr_book_to_read_book(self):

    #     to_be_read_book_in_library = model.BookInLibrary.query.filter(model.BookInLibrary.to_be_read == True).first()
    #     result = self.client.post('/mark-as-read',
    #                               data = {'title': to_be_read_book_in_library.book.title,
    #                                       'subtitle': to_be_read_book_in_library.book.subtitle,
    #                                       'authors': to_be_read_book_in_library.book.authors,
    #                                       'image_link': to_be_read_book_in_library.book.image_link,
    #                                       'categories': to_be_read_book_in_library.book.categories,
    #                                       'description': to_be_read_book_in_library.book.description,
    #                                       'isbn_13': to_be_read_book_in_library.book.isbn_13})

    #     self.assertEqual(200, result.status_code)
    #     updated_book_in_library = model.BookInLibrary.query.get((3,1))
    #     self.assertEqual(True, updated_book_in_library.read)
    #     self.assertEqual(datetime, type(updated_book_in_library.read_date))
    #     self.assertEqual(False, updated_book_in_library.to_be_read)
    #     self.assertEqual(None, updated_book_in_library.to_be_read_date)
    #     self.assertEqual(False, updated_book_in_library.liked)
    #     self.assertEqual(None, updated_book_in_library.liked_date)


    # def test_updating_read_book_as_liked(self):

    #     read_book_in_library = model.BookInLibrary.query.filter(model.BookInLibrary.read == True).first()
    #     result = self.client.post('/mark-as-liked',
    #                               data = {'title': read_book_in_library.book.title,
    #                                       'subtitle': read_book_in_library.book.subtitle,
    #                                       'authors': read_book_in_library.book.authors,
    #                                       'image_link': read_book_in_library.book.image_link,
    #                                       'categories': read_book_in_library.book.categories,
    #                                       'description': read_book_in_library.book.description,
    #                                       'isbn_13': read_book_in_library.book.isbn_13})

    #     self.assertEqual(200, result.status_code)
    #     updated_book_in_library = model.BookInLibrary.query.get((1,1))
    #     self.assertEqual(True, updated_book_in_library.read)
    #     self.assertEqual(datetime, type(updated_book_in_library.read_date))
    #     self.assertEqual(True, updated_book_in_library.liked)
    #     self.assertEqual(datetime, type(updated_book_in_library.liked_date))
    #     self.assertEqual(False, updated_book_in_library.to_be_read)
    #     self.assertEqual(None, updated_book_in_library.to_be_read_date)


    # def test_changing_tbr_book_to_liked_book(self):

    #     to_be_read_book_in_library = model.BookInLibrary.query.filter(model.BookInLibrary.to_be_read == True).first()
    #     result = self.client.post('/mark-as-liked',
    #                               data = {'title': to_be_read_book_in_library.book.title,
    #                                       'subtitle': to_be_read_book_in_library.book.subtitle,
    #                                       'authors': to_be_read_book_in_library.book.authors,
    #                                       'image_link': to_be_read_book_in_library.book.image_link,
    #                                       'categories': to_be_read_book_in_library.book.categories,
    #                                       'description': to_be_read_book_in_library.book.description,
    #                                       'isbn_13': to_be_read_book_in_library.book.isbn_13})

    #     self.assertEqual(200, result.status_code)
    #     updated_book_in_library = model.BookInLibrary.query.get((3,1))
    #     self.assertEqual(True, updated_book_in_library.read)
    #     self.assertEqual(datetime, type(updated_book_in_library.read_date))
    #     self.assertEqual(True, updated_book_in_library.liked)
    #     self.assertEqual(datetime, type(updated_book_in_library.liked_date))
    #     self.assertEqual(False, updated_book_in_library.to_be_read)
    #     self.assertEqual(None, updated_book_in_library.to_be_read_date)


    # def test_changing_liked_book_to_tbr_book(self):

    #     liked_book_in_library = model.BookInLibrary.query.filter(model.BookInLibrary.liked == True).first()
    #     result = self.client.post('/mark-as-to-be-read',
    #                               data = {'title': liked_book_in_library.book.title,
    #                                       'subtitle': liked_book_in_library.book.subtitle,
    #                                       'authors': liked_book_in_library.book.authors,
    #                                       'image_link': liked_book_in_library.book.image_link,
    #                                       'categories': liked_book_in_library.book.categories,
    #                                       'description': liked_book_in_library.book.description,
    #                                       'isbn_13': liked_book_in_library.book.isbn_13})

    #     self.assertEqual(200, result.status_code)
    #     updated_book_in_library = model.BookInLibrary.query.get((2,1))
    #     self.assertEqual(True, updated_book_in_library.to_be_read)
    #     self.assertEqual(datetime, type(updated_book_in_library.to_be_read_date))
    #     self.assertEqual(False, updated_book_in_library.read)
    #     self.assertEqual(None, updated_book_in_library.read_date)
    #     self.assertEqual(False, updated_book_in_library.liked)
    #     self.assertEqual(None, updated_book_in_library.liked_date)


    # def test_removing_read_book_from_user_library(self):

    #     result = self.client.post('/handle-remove-read-book',
    #                               data = {'isbn_13' : '9780804177777'},
    #                                       follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     book = model.Book.query.filter(model.Book.isbn_13 == '9780804177777').first()
    #     deleted_book = model.BookInLibrary.query.filter(model.BookInLibrary.book_id == book.book_id, model.BookInLibrary.user_id ==1).first()
    #     self.assertEqual(None, deleted_book)


    # def test_removing_liked_book_from_user_library(self):

    #     result = self.client.post('/handle-remove-liked-book',
    #                               data = {'isbn_13' : '9780804177778'},
    #                                       follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     book = model.Book.query.filter(model.Book.isbn_13 == '9780804177778').first()
    #     updated_book = model.BookInLibrary.query.filter(model.BookInLibrary.book_id == book.book_id, model.BookInLibrary.user_id == 1).first()
    #     self.assertEqual(False, updated_book.liked)
    #     self.assertEqual(True, updated_book.read)
    #     self.assertEqual(False, updated_book.to_be_read)


    # def test_removing_to_be_read_book_from_user_library(self):

    #     result = self.client.post('/handle-remove-to-be-read-book',
    #                               data = {'isbn_13' : '9780804177779'},
    #                                       follow_redirects=True)
    #     self.assertEqual(200, result.status_code)
    #     book = model.Book.query.filter(model.Book.isbn_13 == '9780804177779').first()
    #     deleted_book = model.BookInLibrary.query.filter(model.BookInLibrary.book_id == book.book_id, model.BookInLibrary.user_id ==1).first()
    #     self.assertEqual(None, deleted_book)


    # def test_create_bookshelf(self):

    #     result = self.client.post('/create-bookshelf.json',
    #                               data = {'bookshelfName': 'Magical Realism'})
    #     self.assertIn(b'Magical Realism', result.data)

    # def test_show_bookshelf_details(self):

    #     result = self.client.get('/Magical-Realism-bookshelf')

    #     self.assertEqual(200, result.response_code)





if __name__ == '__main__':
    unittest.main()