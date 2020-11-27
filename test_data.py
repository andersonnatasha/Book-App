from model import db, User, Book, Author, Category, BookCategory, Bookshelf, BookInLibrary, BookOnBookshelf, BookAuthor, Interest, UserInterest, connect_to_db
from datetime import datetime
from server import app

from faker import Faker
fake = Faker()


def test_data():
    """Create sample data to use for testing the database."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Bookshelf.query.delete()
    BookInLibrary.query.delete()
    BookOnBookshelf.query.delete()
    UserInterest.query.delete()

    # Add sample user
    user1 = User(email='user1@test.com',
                password='test',
                profile_name='Profile Name 1',
                birthday=datetime.strptime(fake.date(), '%Y-%m-%d'),
                gender='Female',
                time_created=datetime.now())
    user2 = User(email='user2@test.com',
                password='test',
                profile_name='Profile Name 2',
                birthday=datetime.strptime(fake.date(), '%Y-%m-%d'),
                gender='Female',
                time_created=datetime.now(),
                login_occurrences=1)

    db.session.add_all([user1, user2])
    db.session.commit()

