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

    book1 = Book(title = 'Test Title1',
                subtitle = None,
                image_link = None,
                description = None,
                isbn_13 = '9780804177777')

    book2 = Book(title = 'Test Title2',
                subtitle = None,
                image_link = None,
                description = None,
                isbn_13 = '9780804177778')

    book3 = Book(title = 'Test Title3',
                subtitle = None,
                image_link = None,
                description = None,
                isbn_13 = '9780804177779')

    author1 = Author(full_name = 'Octavia Thomas', book_id = 1)


    author2 = Author(full_name = 'Matt Reed', book_id = 2)

    author3 = Author(full_name = 'Zora Lane', book_id = 3)

    bookauthor1 = BookAuthor(book_id = 1, author_id = 1)

    bookauthor2 = BookAuthor(book_id = 2, author_id = 2)

    bookauthor3 = BookAuthor(book_id = 3, author_id = 3)

    read_book_in_library = BookInLibrary(book_id = 1,
                                         user_id = 1,
                                         read = True,
                                         read_date = datetime.now(),
                                         liked = False,
                                         liked_date = None,
                                         to_be_read = False,
                                         to_be_read_date = None)

    liked_book_in_library = BookInLibrary(book_id = 2,
                                         user_id = 1,
                                         read = True,
                                         read_date = datetime.now(),
                                         liked = True,
                                         liked_date = datetime.now(),
                                         to_be_read = False,
                                         to_be_read_date = None)


    to_be_read_book_in_library = BookInLibrary(book_id = 3,
                                         user_id = 1,
                                         read = False,
                                         read_date = None,
                                         liked = False,
                                         liked_date = None,
                                         to_be_read = True,
                                         to_be_read_date = datetime.now())


    magical_realism_bookshelf = Bookshelf(name = 'Magical Realism',
                                          user_id = 1,
                                          time_created = datetime.now())

    book_on_magical_realism_bookshelf = BookOnBookshelf(bookshelf_id = 1,
                                                        book_id = 1,
                                                        user_id = 1,
                                                        date_added = datetime.now())

    db.session.add_all([user1, user2, book1, book2, book3,
                        author1, author2, author3,
                        bookauthor1, bookauthor2, bookauthor3,
                        read_book_in_library, liked_book_in_library, to_be_read_book_in_library,
                        magical_realism_bookshelf, book_on_magical_realism_bookshelf])
    db.session.commit()







    # db.session.commit()



