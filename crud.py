"""CRUD operations"""

from model import db, User, Book, Author, Category, BookCategory, Bookshelf, BookInLibrary, BookOnBookshelf, BookAuthor, Interest, UserInterest, connect_to_db
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


def get_user_by_id(user_id):
    """Return user by user id."""

    return User.query.get(user_id)


def get_user_by_email(user_email):
    """Return a user by email."""

    return User.query.filter(User.email == user_email).first()


def get_user_login_frequency(user):
    """Return number of times user has logged in."""

    return user.login_frequency


def log_login_occurrence(user):
    """Add one to user login_frequency."""

    if user.login_frequency == None:
        user.login_frequency = 0
    else:
        user.login_frequency =+ 1

    db.session.add(user)
    db.session.commit()


def create_book(title, subtitle, description, image_link, isbn_13):
    """Create and return a new book."""

    book = Book(title = title,
                subtitle = subtitle,
                description = description,
                image_link = image_link,
                isbn_13=isbn_13)

    db.session.add(book)
    db.session.commit()

    return book


def get_book_by_isbn_13(isbn_13):
    """Return a book by title."""

    return Book.query.filter(Book.isbn_13==isbn_13).first()


def create_author(full_name):
    """Create and return an author."""

    author = Author(full_name = full_name)

    db.session.add(author)
    db.session.commit()

    return author


def get_author_by_full_name(author_full_name):
    """Return author by by full_name."""

    return Author.query.filter(Author.full_name==author_full_name).first()


def create_book_author(book_id, author_id):
    """Create and return an author for a specific book."""

    book_author = BookAuthor(book_id = book_id, author_id = author_id)

    db.session.add(book_author)
    db.session.commit()

    return book_author


def get_book_author(book_id, author_id):
    """Return a bookauthor."""

    book_id = book_id
    author_id = author_id

    book_author = BookAuthor.query.get((book_id, author_id))

    return book_author


def create_category(category):
    """Create and return a category."""

    category = Category(category = category)

    db.session.add(category)
    db.session.commit()

    return category


def get_category_by_name(category):
    """Return a category by its name."""

    category = Category.query.filter(Category.category == category).first()

    return category


def create_book_category(book_id, category_id):
    """Create and return a category for a specific book."""

    book_category = BookCategory(book_id = book_id, category_id = category_id)

    db.session.add(book_category)
    db.session.commit()

    return book_category


def get_book_category(book_id, category_id):
    """Return a bookauthor."""

    book_id = book_id
    category_id = category_id

    book_category = BookCategory.query.get((book_id, category_id))

    return book_category


def create_a_book_in_library(book, user_id):
    """Create and return a book in a user library."""

    book_in_library = BookInLibrary(book = book, user_id = user_id)

    db.session.add(book_in_library)
    db.session.commit()

    return book_in_library


def get_book_in_library(book, user_id):
    """ Gets a book in a library by title user id."""

    book_id = book.book_id
    book_in_library = BookInLibrary.query.get((book_id, user_id))

    return book_in_library


def delete_book_from_library(book_in_library):
    """Delete read book from user library."""

    db.session.delete(book_in_library)
    db.session.commit()


def create_a_book_on_a_bookshelf(book_in_library, bookshelf):
    """Add a book to a users particular bookshelf."""

    book_on_bookshelf = BookOnBookshelf(book_id=book_in_library.book.book_id, bookshelf_id=bookshelf.bookshelf_id, user_id=book_in_library.user_id)

    db.session.add(book_on_bookshelf)
    db.session.commit()

    return book_on_bookshelf

def get_book_on_bookshelf(book_in_library, bookshelf):
    """Get a book on a users particular bookshelf."""

    book_id = book_in_library.book.book_id
    bookshelf_id = bookshelf.bookshelf_id

    book_on_bookshelf = BookOnBookshelf.query.filter(BookOnBookshelf.book_id==book_id, BookOnBookshelf.bookshelf_id==bookshelf_id).first()

    return book_on_bookshelf

def mark_book_as_read(book_in_library, read_status_update, liked_status):
    """Update book tags to indicate book is categorized as read."""

    # The first time a book has been marked as read
    if (book_in_library.read == None) and (book_in_library.to_be_read == None):
        book_in_library.read = True
        book_in_library.read_date = datetime.now()
        book_in_library.liked = False
        book_in_library.liked_date = None
        book_in_library.to_be_read = False
        book_in_library.to_be_read_date = None

    # Book already in library: Book is on TBR list and moving to read/liked list
    elif (book_in_library.read == False) and (read_status_update == True) and (liked_status == False):
        book_in_library.read = True
        book_in_library.read_date = datetime.now()
        book_in_library.to_be_read = False
        book_in_library.to_be_read_date = None

    # # Book already in library: book is on TRB list and moving to read list, but not liked list
    # elif (book_in_library.read == False) and (read_status_update == True):
    #     book_in_library.read = True
    #     book_in_library.read_date = datetime.now()
    #     book_in_library.liked = False
    #     book_in_library.liked_date = None
    #     book_in_library.to_be_read = False
    #     book_in_library.to_be_read_date = None

    db.session.add(book_in_library)
    db.session.commit()


def mark_book_as_liked(book_in_library, read_status_update, liked_status):
    """Update book tags to indicate book is categorized as liked."""

    # The first time a book has been marked as liked
    if (book_in_library.read == None) and (book_in_library.to_be_read == None):
        book_in_library.liked = True
        book_in_library.liked_date = datetime.now()
        book_in_library.read = True
        book_in_library.read_date = datetime.now()
        book_in_library.to_be_read = False
        book_in_library.to_be_read_date = None

    # Book already in library: Book is on TBR list and moving to read/liked list
    elif (book_in_library.read == False) and (liked_status == True):
        book_in_library.read = True
        book_in_library.read_date = datetime.now()
        book_in_library.liked = True
        book_in_library.liked_date = datetime.now()
        book_in_library.to_be_read = False
        book_in_library.to_be_read_date = None

    # Book in library: book is read, but not liked, being added to liked list
    elif (book_in_library.read == True) and (liked_status == True):
        book_in_library.liked = True
        book_in_library.liked_date = datetime.now()

    db.session.add(book_in_library)
    db.session.commit()


def mark_book_as_to_be_read(book_in_library, read_status_update, liked_status):
    """Update book tags to indicate book is categorized as to be read"""

    # The first time a book has been marked as tbr
    if (book_in_library.read == None) and (book_in_library.to_be_read == None):
        book_in_library.to_be_read = True
        book_in_library.to_be_read_date = datetime.now()
        book_in_library.read = False
        book_in_library.read_date = None
        book_in_library.liked = False
        book_in_library.liked_date = None

    # Book in library: Book is read, possibly liked, and moving to tbr list
    elif (book_in_library.read == True) and (read_status_update == False):
        book_in_library.read = False
        book_in_library.read_date = None
        book_in_library.liked = False
        book_in_library.liked_date = None
        book_in_library.to_be_read = True
        book_in_library.to_be_read_date = datetime.now()

    db.session.add(book_in_library)
    db.session.commit()


def remove_liked_tag(book_in_library, read_status_update, liked_status):
    """Change a liked tag from True to False."""

    # Book in library: book is liked, and liked tag is being removed
    book_in_library.liked = False
    book_in_library.liked_date = None
    db.session.add(book_in_library)
    db.session.commit()


def get_read_books_by_user_id(user_id):
    """Get read books in a user's library by a user id."""

    user = User.query.get(user_id)
    read_books_in_library = BookInLibrary.query.filter((BookInLibrary.user_id == user.user_id ) & (BookInLibrary.read == True)).all()

    return read_books_in_library


def get_liked_books_by_user_id(user_id):
    """Get liked books in a user's library by a user id."""

    user = User.query.get(user_id)
    liked_books_in_library = BookInLibrary.query.filter((BookInLibrary.user_id == user.user_id ) & (BookInLibrary.liked == True)).all()

    return liked_books_in_library


def get_to_be_read_books_by_user_id(user_id):
    """Return to be read books in a user's library by a user id."""

    user = User.query.get(user_id)
    to_be_read_books_in_library = BookInLibrary.query.filter((BookInLibrary.user_id == user.user_id ) & (BookInLibrary.to_be_read == True)).all()

    return to_be_read_books_in_library


def get_read_book_by_isbn_13(isbn_13, user_id):
    """Return a read book by title and user_id."""

    book = Book.query.filter((Book.isbn_13 == isbn_13) & (BookInLibrary.read == True)).first()
    book_id = book.book_id

    return BookInLibrary.query.get((book_id, user_id))


def get_liked_book_by_isbn_13(isbn_13, user_id):
    """Return a liked book by it's title and user."""

    book = Book.query.filter((Book.isbn_13 == isbn_13) & (BookInLibrary.liked == True)).first()
    # book_id = book.book_id

    return (book)


def get_to_be_read_book_by_isbn_13(isbn_13, user_id):
    """Return a to be read book by it's title and user."""

    book = Book.query.filter((Book.title==isbn_13) & (BookInLibrary.to_be_read == True)).first()

    return BookInLibrary.query.get((book.book_id, user_id))


def create_bookshelf(name, user_id):
    """"Create and return a user's bookshelf."""

    time_created = datetime.now()
    bookshelf = Bookshelf(name = name, user_id = user_id, time_created = time_created)

    db.session.add(bookshelf)
    db.session.commit()

    return bookshelf


def get_user_bookshelves(user_id):
    """Return all bookshelves for a particular user."""

    return Bookshelf.query.filter(Bookshelf.user_id==user_id).all()


def get_a_bookshelf(user_id, bookshelf_name):
    """Return a particular bookshelf by the shelf name and user id."""

    user_id = user_id
    bookshelf_name = bookshelf_name

    return Bookshelf.query.filter(Bookshelf.name==bookshelf_name, Bookshelf.user_id==user_id ).first()


def create_interest(interest):
    """Create and return an interest."""

    interest = Interest(interest = interest)

    db.session.add(interest)
    db.session.commit()

    return interest


def get_interest_by_name(interest):
    """Return a interest by its name."""

    interest = Interest.query.filter(Interest.interest == interest).first()

    return interest


def create_user_interest(user_id, interest_id):
    """Create and return a interest for a specific user."""

    user_interest = UserInterest(user_id = user_id, interest_id = interest_id)

    db.session.add(user_interest)
    db.session.commit()

    return user_interest


def get_user_interest(user_id, interest_id):
    """Return a userinterest by a user id."""

    user_id = user_id
    interest_id = interest_id

    user_interest = UserInterest.query.get((user_id, interest_id))

    return user_interest


def get_all_interests_for_user(user_id):
    """Return a userinterest by a user id."""

    user = User.query.get(user_id)

    return user.interests


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


