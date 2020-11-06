"""CRUD operations"""

from model import db, User, Book, BookCopy, Author, Category, BookCategory, connect_to_db


def create_user(email, password, full_name, birthday, created_at, gender=None):
    """Create and return a new user."""

    user = User(email=email,
                password=password,
                full_name=full_name,
                birthday=birthday,
                created_at=created_at,
                gender=gender)

    db.session.add(user)
    db.session.commit()

    return user

def create_book(title, liked=None, categories=None):
    """Create and return a new book."""

    book = Book(title=title,
                liked=liked,
                catrgories=categories)

    db.session.add(book)
    db.session.commit()

    return book


def create_book_copy(book):
    """Create and return a copy of a particular book."""

    book_copy = BookCopy(book=book)

    db.session.add(book_copy)
    db.session.commit()

    return book_copy


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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


