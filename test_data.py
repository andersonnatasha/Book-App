from model import db, User, Book, Author, Category, BookCategory, Bookshelf, BookInLibrary, BookAuthor, Interest, UserInterest, connect_to_db

from faker import Faker
fake = Faker()


def test_data():
    """Create sample data to use for testing the database."""

    # In case this is run more than once, empty out existing data 
    User.query.delete()

    # Add sample user
    user = User(email='user1@test.com', password='test')


    