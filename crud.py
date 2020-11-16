"""CRUD operations"""

from model import db, User, Book, Author, Category, BookCategory, Bookshelf, BookInLibrary, BookAuthor, connect_to_db
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
    """Return user by user id"""

    return User.query.get(user_id)

def get_user_by_email(user_email):
    """Return a user by email"""

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
    """Return a book by title"""

    return Book.query.filter(Book.isbn_13==isbn_13).first()


def create_author(full_name):
    """Create and return an author."""

    author = Author(full_name = full_name)

    db.session.add(author)
    db.session.commit()

    return author


def get_author_by_full_name(author_full_name):
    """Return author by by full_name"""

    return Author.query.filter(Author.full_name==author_full_name).first()


def create_book_author(book_id, author_id):
    """Create and return an author for a specific book"""

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
    """Return a category by its name"""

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

    book_in_library = BookInLibrary(book = book, user_id = user_id)

    db.session.add(book_in_library)
    db.session.commit()

    return book_in_library

def get_book_in_library(book, user_id):
    """ Gets a book in a library by title user id"""

    isbn_13 = book.isbn_13
    book_id = book.book_id
    book_in_library = BookInLibrary.query.get((book_id, user_id))

    return book_in_library

def delete_book_from_library(book_in_library):
    """Delete read book from user library."""

    db.session.delete(book_in_library)
    db.session.commit()

    # if removing a read book


    # if removing a liked book

    # if removing a tbr book




def create_read_book(user_id, book_id, read, read_date):
    """Create a read book in a user library"""

    read_book = BookInLibrary(user_id = user_id,
                              book_id = book_id,
                              read = read,
                              read_date = read_date)


    db.session.add(read_book)
    db.session.commit()

    return read_book

# def create_liked_book(user_id, book_id, liked, liked_date):
#     """Create a liked book in a user library"""

#     liked_book = BookInLibrary(user_id = user_id,
#                               book_id = book_id,
#                               liked = liked,
#                               liked_date = liked_date)

#     db.session.add(liked_book)
#     db.session.commit()

#     return liked_book



def update_book_tags(book_in_library, read_status_update, liked_status):


    # The first time a book has been marked as read/tbr/liked
    if (book_in_library.read == None) and (book_in_library.to_be_read == None):
        if read_status_update == True:
            book_in_library.read = True
            book_in_library.read_date = datetime.now() #showing up as None
            book_in_library.to_be_read = False
            if liked_status == True:
                book_in_library.liked = True
                book_in_library.liked_date = datetime.now()
            else:
                book_in_library.liked = False
        else:
            book_in_library.to_be_read = True
            book_in_library.to_be_read_date = datetime.now()
            book_in_library.read = False
            book_in_library.liked = False

        db.session.add(book_in_library)
        db.session.commit()
        print("========================")
        print("========================")
        print("========================")
        print("========================")
        print("========================")
        print(book_in_library.book.title)
        print(f'read :{book_in_library.read}')
        print(f'TBR :{book_in_library.to_be_read}')
        print("if (book_in_library.read == None) and (book_in_library.to_be_read == None) ")
        print("========================")
        print("========================")


    # Book already in library: Book is TRB and changing to add to read list
    elif (book_in_library.read == False) and (read_status_update == True) and (liked_status == False):
        book_in_library.read = True
        book_in_library.read_date = datetime.now()
        book_in_library.liked = False
        book_in_library.to_be_read = False
        book_in_library.to_be_read_date = None
        db.session.add(book_in_library)
        db.session.commit()
        print("========================")
        print("========================")
        print("========================")
        print("========================")
        print(book_in_library)
        print("elif (book_in_library.read == False) and (read_status_update == True) and (liked_status == False)")
        print("========================")
        print("========================")

    # Book already in library: Book is on TBR list and moving to read/liked list
    elif (book_in_library.read == False) and (liked_status == True):
        book_in_library.read = True
        book_in_library.read_date = datetime.now()
        book_in_library.liked = True
        book_in_library.liked_date = datetime.now()
        book_in_library.to_be_read = False
        book_in_library.to_be_read_date = None
        db.session.add(book_in_library)
        db.session.commit()
        print("========================")
        print("========================")
        print("========================")
        print("========================")
        print(book_in_library.book.title)
        print("elif (book_in_library.read == False) and (read_status_update == True) and (liked_status == True):")


    # Book alreay in library: book is on TRB list and moving to read list, but not liked list
    elif (book_in_library.read == False) and (read_status_update == True):
        book_in_library.read = True
        book_in_library.read_date = datetime.now()
        book_in_library.liked = False
        book_in_library.liked_date = None
        book_in_library.to_be_read = False
        book_in_library.to_be_read_date = None
        db.session.add(book_in_library)
        db.session.commit()
        print("========================")
        print("========================")
        print("========================")
        print("========================")
        print(book_in_library.book.title)
        print("elif (book_in_library.read == False) and (read_status_update == True):")

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
        print("========================")
        print("========================")
        print("========================")
        print("========================")
        print("elif (book_in_library.read == True) and (read_status_update == False):")


    # Book in library: book is liked, and liked tag is being removed
    elif (book_in_library.liked == True) and (liked_status == False):
        book_in_library.liked = False
        book_in_library.liked_date = None
        db.session.add(book_in_library)
        db.session.commit()


    # Book in library: book is read, but unliked, being added to liked list
    elif (book_in_library.read == True) and (liked_status == True):
        book_in_library.liked = True
        book_in_library.liked_date = datetime.now()
        db.session.add(book_in_library)
        db.session.commit()
        print("========================")
        print("========================")
        print("========================")
        print("========================")
        print("elif (book_in_library.read == True) and (read_status_update == False):")


    #     print("===============================")
    #     print("===============================")
    #     print("===============================")
    #     print(book_in_library.book.title)
    #     print(f'to be read:{book_in_library.to_be_read}')
    #     print(f'to be read time: {book_in_library.to_be_read_date}')
    #     print(f'read: {book_in_library.read}')
    #     print(f'read time: {book_in_library.read_date}')
    #     print(f'liked: {book_in_library.liked}')
    #     print(f'liekd time: {book_in_library.liked_date}')
    #     print("===============================")
    #     print("===============================")
    #     print("===============================")






    # if (book_in_library.read == None) and (book_in_library.to_be_read == None):
    #     if read_status_update == True:
    #         book_in_library.read = True
    #         book_in_library.read_date = datetime.now() #showing up as None
    #         print("In if statement under read_DATE")
    #         book_in_library.to_be_read = False
    #         book_in_library.to_be_read_date = None
    #         if liked_status == True:
    #             print("In if statement LIKED STATUS IS TRUE")
    #             book_in_library.liked = True
    #             book_in_library.liked_date = datetime.now()
    #         else:
    #             print("In if statement LIKED STATUS IS FAAALLLLSSEEEE")
    #     else:
    #         book_in_library.to_be_read = True
    #         book_in_library.to_be_read_date = datetime.now()
    #         book_in_library.read = False
    #         book_in_library.read_date = None
    #         book_in_library.liked = False
    #         book_in_library.liked_date = None

    # db.session.add(book_in_library)
    # db.session.commit()


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
    """Return to be read books in a user's library by a user id"""

    user = User.query.get(user_id)
    to_be_read_books_in_library = BookInLibrary.query.filter((BookInLibrary.user_id == user.user_id ) & (BookInLibrary.to_be_read == True)).all()

    return to_be_read_books_in_library

def get_read_book_by_isbn_13(isbn_13, user_id):
    """Return a read book by title and user_id"""

    book = Book.query.filter((Book.isbn_13 == title) & (BookInLibrary.read == True)).first()
    book_id = book.book_id

    return BookInLibrary.query.get((book_id, user_id))

def get_liked_book_by_isbn_13(isbn_13, user_id):
    """Return a liked book by it's title and user"""

    book = Book.query.filter((Book.isbn_13 == isbn_13) & (BookInLibrary.liked == True)).first()
    # book_id = book.book_id

    return ((book))


def get_to_be_read_book_by_isbn_13(isbn_13, user_id):
    """Return a to be read book by it's title and user"""

    book = Book.query.filter((Book.title==isbn_13) & (BookInLibrary.to_be_read == True)).first()

    return BookInLibrary.query.get((book.book_id, user_id))


def create_bookshelf(name, user):
    """"Create and return a user's bookshelf"""

    bookshelf = Bookshelf(name=name, user=user)

    db.session.add(bookshelf)
    db.session.commit()

    return bookshelf


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


