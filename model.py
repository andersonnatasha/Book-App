"""Models for book app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True
                        )
    email = db.Column(db.String(50),
                     nullable=False,
                     unique=True
                     )
    full_name = db.Column(db.String(50),
                          nullable=False)
    gender = db.Column(db.String(17))
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


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

    def __repr__(self):
        return f'<Book book_id={self.book_id} title={self.title}'


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

    def __repr__(self):
        f'<Author author_id={self.author_id} lname={self.lname}>'


class Category(db.Model):
    """A book category"""

    __tablename__ = 'categories'

    category_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True
                            )
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        f'<Category category_id={self.category_id} category={self.category}>'


class BookCategory(db.Model):
    """Category of a specific book"""

    __tablename__ = 'books_categories'

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
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))


class ToBeReadCollection(db.Model):
    """A collection of books the user wants to read"""

    __tablename__ = 'tbr_collections'

    tbr_collection_id = db.Column(db.Integer,
                                  primary_key=True,
                                  autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))


def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__=='__main__':
    from server import app

    connect_to_db(app)
