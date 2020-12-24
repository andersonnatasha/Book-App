"""Models for book app"""

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
                     unique=True,
                     nullable=False,
                     )
    password = db.Column(db.String(25),
                         nullable=False,
                         )
    profile_name = db.Column(db.String(50),
                         nullable=False
                          )
    birthday = db.Column(db.Date, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(17))
    login_occurrences = db.Column(db.Integer)

    books_in_library = db.relationship('BookInLibrary')
    bookshelves = db.relationship('Bookshelf')
    interests = db.relationship('Interest',
                                secondary='users_interests',
                                backref='users')

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Book(db.Model):
    """A book."""

    __tablename__ = 'books'

    book_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True
                        )
    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(200))
    description = db.Column(db.Text)

    isbn_13 = db.Column(db.String(13))
    image_link = db.Column(db.String(350))

    authors = db.relationship('Author',
                              secondary="books_authors",
                              backref='books')
    categories = db.relationship('Category',
                                 secondary="books_categories",
                                 backref='books'
                                )

    def __repr__(self):
        return f'<Book book_id={self.book_id} title={self.title}>'


class Author(db.Model):
    """An author."""

    __tablename__ = 'authors'

    author_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True
                          )
    full_name = db.Column(db.String(150),
                      nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))

    book = db.relationship('Book')

    def __repr__(self):
        return f'<Author author_id={self.author_id} full_name={self.full_name}>'

class BookAuthor(db.Model):
    """A book and author combination."""

    __tablename__ = 'books_authors'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True,)
    author_id = db.Column(db.Integer,
                         db.ForeignKey('authors.author_id'),
                         primary_key=True,)

    book = db.relationship('Book')
    author = db.relationship('Author')

    def __repr__(self):
        return f'<BookAuthor book_id={self.book_id} author_id={self.author_id}>'


class Category(db.Model):
    """A book category."""

    __tablename__ = 'categories'

    category_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True
                            )
    category = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Category category_id={self.category_id} category={self.category}>'


class BookCategory(db.Model):
    """Category of a specific book."""

    __tablename__ = 'books_categories'

    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        primary_key=True
                        )
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.category_id'),
                            primary_key=True
                            )

    book = db.relationship('Book')
    category =db.relationship('Category')

    def __repr__(self):
        return f'<BookCategory book_id={self.book_id} category_id={self.category_id}>'


class RecommendedBook(db.Model):
    """A recommended book for a user."""

    __tablename__ = 'recommended_books'

    recommended_book_id = db.Column(db.Integer,
                                     primary_key=True,
                                     autoincrement=True
                                    )
    book_id = db.Column(db.Integer,
                         db.ForeignKey('books.book_id')
                         )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id')
                        )
    def __repr__(self):
        return f'<RecommendedBook recommended_book_id={self.recommended_book_id}>'


class Bookshelf(db.Model):
    """A user's bookself."""

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
    time_created = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Bookshelf bookshelf_id={self.bookshelf_id} name={self.name}>'


class BookInLibrary(db.Model):
    """A book in a particular user library."""

    __tablename__ = 'books_in_library'

    book_id = db.Column(db.Integer,
                         db.ForeignKey('books.book_id'),
                         primary_key=True
                         )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        primary_key=True
                        )
    notes = db.Column(db.Text)
    read = db.Column(db.Boolean)
    read_date = db.Column(db.DateTime) # date read tag was added
    liked  = db.Column(db.Boolean)
    liked_date = db.Column(db.DateTime) # date liked tag was added
    to_be_read = db.Column(db.Boolean)
    to_be_read_date = db.Column(db.DateTime) #date to be read tag was added

    book = db.relationship('Book')
    user = db.relationship('User')

    def __repr__(self):
        return f'<BookInLibrary book_id={self.book_id} book_title={self.book.title} user_id={self.user_id}>'


class BookOnBookshelf(db.Model):
    """A book in a particular book self."""

    __tablename__ = 'books_on_bookshelves'

    book_on_bookshelf_id = db.Column(db.Integer,
                                     primary_key=True,
                                     autoincrement=True
                                    )
    bookshelf_id = db.Column(db.Integer,
                            db.ForeignKey('bookshelves.bookshelf_id'),
                            )
    book_id = db.Column(db.Integer,
                         db.ForeignKey('books.book_id')
                         )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id')
                        )
    date_added = db.Column(db.DateTime)

    user = db.relationship('User')
    book = db.relationship('Book')
    bookshelf = db.relationship('Bookshelf')


    def __repr__(self):
        return f'<BookOnBookshelf book_on_bookshelf_id={self.book_on_bookshelf_id} bookshelf={self.bookshelf_id}>'


class Interest(db.Model):
    """An interest"""

    __tablename__ = 'interests'

    interest_id = db.Column(db.Integer,
                  primary_key=True)
    interest = db.Column(db.String(30))

    def __repr__(self):
        return f'<Interest interest_id={self.interest_id}  interest={self.interest}>'


class UserInterest(db.Model):
    """A user interest"""

    __tablename__ = 'users_interests'

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        primary_key=True
                        )
    interest_id = db.Column(db.Integer,
                        db.ForeignKey('interests.interest_id'),
                        primary_key=True
                        )

    user = db.relationship('User')
    interest = db.relationship('Interest')


    def __repr__(self):
        return f'<UserInterest user_id={self.user_id} interest_id={self.interest_id}>'


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
