"""CRUD operations"""

from model import db, User, Book, Author, Category, BookCategory, Bookshelf, BookInLibrary, connect_to_db
from datetime import datetime


def create_user(email, password, profile_name, birthday, gender, time_created):
    """Create and return a new user."""

    user = User(email = email,
                password = password,
                profile_name = profile_name,
                birthday = birthday,
                gender = gender,
                time_created = time_created)
    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_id(id):
    """Return user by user id"""

    return User.query.get(id)


def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()


def create_book(title):
    """Create and return a new book."""

    book = Book(title=title)

    db.session.add(book)
    db.session.commit()

    return book

def get_book_by_title(title):
    """Return a book by title"""

    return Book.query.filter(Book.title == title).first()


def create_author(full_name, book):
    """Create and return an author."""

    author = Author(full_name = full_name,
                    book = book)

    db.session.add(author)
    db.session.commit()


def create_category(category):
    """Create and return a category."""

    category = Category(category=category)

    db.session.add(category)
    db.session.commit()

    return category


def create_book_category(book, category):
    """Create and return a category for a specific book."""

    book_category = BookCategory(book = book, category = category)

    db.session.add(book_category)
    db.session.commit()

    return book_category

# def create_authors(fname, lname):
#     """Create authors for a particulr book"""


def create_read_book(user_id, book_id, read, read_date):
    """Create a read book in a user library"""

    read_book = BookInLibrary(user_id = user_id,
                              book_id = book_id,
                              read = read,
                              read_date = read_date)

    db.session.add(read_book)
    db.session.commit()

    return read_book


# def create_a_book_in_library(user, book, read, read_date, liked,
#                             liked_date, to_be_read, to_be_read_date):

#     book_in_library = BookInLibrary(user = user,
#                         book = book,
#                         read = read,
#                         read_date = read_date,
#                         liked = liked,
#                         liked_date = liked_date,
#                         to_be_read = to_be_read,
#                         to_be_read_date = to_be_read_date)

#     db.session.add(book_in_library)
#     db.session.commit()

#     return book_in_library


def get_read_books_by_user_id(user_id):
    """Get read books in a user's library by a user id"""

    user = User.query.get(user_id)
    read_books_in_library = BookInLibrary.query.filter((BookInLibrary.user_id == user.user_id ) & (BookInLibrary.read == True)).all()

    return read_books_in_library

def get_liked_books_by_user_id(user_id):
    """Get liked books in a user's library by a user id"""

    user = User.query.get(user_id)
    liked_books_in_library = BookInLibrary.query.filter((BookInLibrary.user_id == user.user_id ) & (BookInLibrary.liked == True)).all()

    return liked_books_in_library

def get_to_be_read_books_by_user_id(user_id):
    """Return liked books in a user's library by a user id"""

    user = User.query.get(user_id)
    to_be_read_books_in_library = BookInLibrary.query.filter((BookInLibrary.user_id == user.user_id ) & (BookInLibrary.to_be_read == True)).all()

    return to_be_read_books_in_library

def get_read_book_by_title(title, user_id):
    """Return a read book by title"""

    book = Book.query.filter(Book.title==title).first()
    book_id = book.book_id

    return BookInLibrary.query.get((book_id, user_id))


def create_bookshelf(name, user):
    """"Create and return a user's bookshelf"""

    bookshelf = Bookshelf(name=name, user=user)

    db.session.add(bookshelf)
    db.session.commit()

    return bookshelf


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


