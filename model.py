"""Models for book app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True
                        )
    email = db.Column(db.String(50),
                     unique=True,
                     nullable=False,
                     )
    password = db.Column(db.String(25),
                         nullable=False,
                         )
    full_name = db.Column(db.String(50),
                         nullable=False
                          )
    birthday = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(17))

    read_book_collection = db.relationship('ReadBooksCollection')

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
    liked = db.Column(db.Boolean)
    categories = db.relationship('Category',
                                 secondary="books_categories",
                                 backref='books'
                                 )

    author = db.relationship('Author')
    book_copy = db.relationship('BookCopy')
    book_category = db.relationship('BookCategory')

    def __repr__(self):
        return f'<Book book_id={self.book_id} title={self.title}>'


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
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))

    book = db.relationship('Book')

    def __repr__(self):
        return f'<Author author_id={self.author_id} lname={self.lname}>'


class Category(db.Model):
    """A book category"""

    __tablename__ = 'categories'

    category_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True
                            )
    category = db.Column(db.String(50), nullable=False, unique=True)


    def __repr__(self):
        return f'<Category category_id={self.category_id} category={self.category}>'


class BookCategory(db.Model):
    """Category of a specific book"""

    __tablename__ = 'books_categories'

    book_category_id = db.Column(db.Integer,
                                   primary_key=True,
                                   autoincrement=True
                                   )
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        nullable=False
                        )
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.category_id'),
                            nullable=False
                            )

    book = db.relationship('Book')
    category =db.relationship('Category')

    def __repr__(self):
        return f'<BookCategory book_id={self.book_id} category_id={self.book_category_id}>'


class ReadBook(db.Model):
    """A read book"""

    __tablename__ = 'read_books'

    read_book = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True
                                         )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))

    book_copy = db.relationship('BookCopy')
    user = db.relationship('User')


    def __repr__(self):
        return f'<ReadBook read_book={self.read_book_id} book_copy={self.book_id}>'


class LikedBook(db.Model):
    """A liked book"""

    __tablename__ = 'liked_books'

    liked_book_id = db.Column(db.Integer,
                             primary_key=True,
                             autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))

    book_copy = db.relationship('BookCopy')
    user = db.relationship('User')

    def __repr__(self):
        return f'<LikeBook liked_book_id={self.liked_book_id} user_id={self.user_id}>'


class ToBeReadBook(db.Model):
    """A book to be read"""

    __tablename__ = 'to_be_read_books'

    to_be_read_book_id = db.Column(db.Integer,
                             primary_key=True,
                             autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))

    book_copy = db.relationship('BookCopy')
    user = db.relationship('User')

    def __repr__(self):
        return f'<ToBeReadBook to_be_read_book_id={self.to_be_read_book_id user_id={self.user_id}>'


class Bookshelf(db.Model):
    """A bookself"""

    __tablename__ = 'bookshelves'

    bookshelf_id = db.Column(db.Integer,
                             primary_key=True,
                             autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False
                        )
    book_copy_id = db.Column(db.Integer, db.ForeignKey('book_copies.book_copy_id'))
    #created_at = db.Column(db.DateTime, nullale=False)

    def __repr__(self):
        return f'<Bookshelf bookshelf_id={self.bookshelf_id} name={self.name}>'


def connect_to_db(flask_app, db_uri='postgresql:///bookslibrary', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__=='__main__':
    from server import app

    connect_to_db(app)
