from model import db, User, Book, Author, Category, BookCategory, Bookshelf, BookInLibrary, BookAuthor, Interest, UserInterest, connect_to_db
from datetime import datetime

from faker import Faker
fake = Faker()


def test_data():
    """Create sample data to use for testing the database."""

    # In case this is run more than once, empty out existing data 

    # Add sample user
    user = User(email='user1@test.com', password='test', profile_name='Profile Name 1', birthday=datetime.strptime(fake.date(), '%Y-%m-%d'), gender='Female', time_created  = datetime.now())

    db.session.add(user)
    db.session.commit()
    