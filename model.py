"""Models for book app."""

from flask_sqlalchemy import SQLAlchemy

db = SQAlchemy()


class User(db.Model):
    """A user."""

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
                        autoincrement=True
                        )
    title = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer,
                          db.ForeignKey('authors.author_id'),
                          nullable=False
                          )
    liked = db.Column(db.Boolean)
    categories = db.relationship('Category',
                                 secondary="books_categories",
                                 backref='books'
                                 )


class Author(db.Model):
    """An author"""

    __tablename__ = 'authors'

    author_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True
                          )
    fname = db.Column(db.String(25),
                      nullable=False)
    lname = db.Column(db.String(40),
                      nullable=False
                      )
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        nullable=False
                        )


class Category(db.Model):
    """A book category"""

    __table__ = 'categories'

    category_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True
                            )
    category = db.Column(db.String(50), nullable=False)


class BookCategory(db.Model):
    """Category of a specific book"""

    __table__ = 'books_categories'

    book_categories_id = db.Column(db.Integer,
                                   primary_key=True,
                                   autoincrement=True
                                   )
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    category = db.Column(db.Integer, db.ForeignKey('categories.category_id'))


class ReadBooksCollection(db.Model):
    """A collection of read books"""

    __tablename__ = 'read_books_collections'

    read_books_collection_id = db.Column(db.Integer,
                                         primary_key=True,
                                         autoincrement=True
                                         )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))


class LikedBooksCollection(db.Model):
    """A collection of liked books"""

    __tablename__ = 'liked_books_collections'

    liked_book_collection_id = db.Column(db.Integer,
                                         primary_key=True,
                                         autoincrement=True)