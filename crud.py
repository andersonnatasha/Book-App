"""CRUD operations"""

from model import db, User, Book, Author, Category, BookCategory, BookTagsStatus, Bookshelf, BookInBookshelf, connect_to_db
from datetime import datetime


def create_user(email, password, full_name, birthday, gender, time_created):
    """Create and return a new user."""

    user = User(email=email,
                password=password,
                full_name=full_name,
                birthday=birthday,
                gender=gender,
                time_created=time_created)
    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()


def create_book(title):
    """Create and return a new book."""

    book = Book(title=title
                )

    db.session.add(book)
    db.session.commit()

    return book


def create_author(fname, lname, book):
    """Create and return an author."""

    author = Author(fname=fname,
                    lname=lname,
                    book=book)

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

    book_category = BookCategory(book=book, category=category)

    db.session.add(book_category)
    db.session.commit()

    return book_category


def create_book_tags_status(book, user, read=None, liked=None, to_be_read=None):
    """Create and return a book to be read for a user"""

    book_tags_status = BookTagsStatus(book=book, user=user, read=read,
                                     liked=liked, to_be_read=to_be_read)

    db.session.add(book_tags_status)
    db.session.commit()

    return book_tags_status


def create_bookshelf(name, user):
    """"Create and return a user's bookshelf"""

    bookshelf = Bookshelf(name=name, user=user)

    db.session.add(bookshelf)
    db.session.commit()

    return bookshelf


def create_book_in_bookshelf(book, user):
    """Create book in bookshelf"""

    book_in_bookshelf = BookInBookshelf(book=book, user=user)

    db.session.add(book_in_bookshelf)
    db.session.commit()

    return book_in_bookshelf




if __name__ == '__main__':
    from server import app
    connect_to_db(app)


