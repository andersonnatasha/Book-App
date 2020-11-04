"""Models for book app."""

from flask_sqlalchemy import SQLAlchemy

db = SQAlchemy()


class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True
                        )
    full_name = db.Column(db.String(50),
                          nullable=False)
    email = db.Column(db.String(50),
                     nullable=False)
    gender = db.Column(db.String(17))
    created_at = db.Column(db.DateTime)


class Book(db.Model):
    """A book"""

    __tablename__ = 'books'

    book_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    title = db.Column(db.String(250))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    liked = db.Column(db.Boolean)
    categories = db.relationship('Category',
                                 secondary="book_category",
                                 backref='books')

class Authors(db.Model):
    """An author"""

    __tablename__ = 'authors'

    author_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True)
    fname = db.Column(db.String(25),
                      nullable=False)
    lname = db.Column(db.String(40),
                      nullable=False)


class ReadBooksCollection(db.Model):
    """A collection of read books"""

    __tablename__ = 'read_books_collection'

    read_books_collection_id = db.Column(db.Integer,
                                         primary_key=True,
                                         autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))