from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)

from model import connect_to_db

import crud
import google_books_api

from jinja2 import StrictUndefined

from os import environ

from datetime import datetime

from random import randint

app = Flask(__name__)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

app.secret_key = environ['FLASK_KEY']


@app.route('/')
def homepage():
    """View homepage."""

    user_id = session.get('user_id')
    if user_id:
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]

        search_results = google_books_api.show_recommended_books()
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]
        return render_template('homepage.html',search_results=search_results, bookshelves=bookshelves)

    else:
        bookshelves = None
        return render_template('homepage.html', bookshelves=bookshelves)

@app.route('/sign-up')
def sign_up():
    """Register a user."""


    return render_template('sign_up.html')


@app.route('/handle-sign-up', methods=['POST'])
def handle_sign_up():
    """Register a user."""

    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmed = request.form.get('confirm-password')
    profile_name = request.form.get('profile-name')
    birth_month = request.form.get('birth-month')
    birth_day = request.form.get('birth-day')
    birth_year = request.form.get('birth-year')
    gender = request.form.get('gender')

    time_created = datetime.now()

    birthday = datetime.strptime(f'{birth_month}/{birth_day}/{birth_year}', ('%B/%d/%Y'))

    user = crud.get_user_by_email(email)

    if user:
        flash('Account already exists.')
        return redirect('/sign-up')
    elif password != password_confirmed:
        flash('Passwords do not match.')
        return redirect('/sign-up')
    else:
        crud.create_user(email, password, profile_name,
                        birthday, gender, time_created)
        flash('Account created! Please sign in.')
        return redirect('/log-in')


@app.route('/log-in')
def log_in():
    """User log in."""

    return render_template('log_in.html')

@app.route('/log-out')
def handle_logging_out():
    """Log a user out."""

    session['user_id'] = None

    return redirect("/")


@app.route('/log-in-credentials', methods=['POST'])
def validate_login_credentials():

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user == None or user.password != password:
        flash(f'The email and password you entered did not match our records. Please double-check and try again.')
        return redirect('/log-in')
    else:
        session['user_id'] = user.user_id
        user_id = session['user_id']

        session['profile_name'] = user.profile_name
        user = crud.get_user_by_id(user_id)

        login_occurrences = crud.get_user_login_occurrences(user)
        if login_occurrences == None:
            crud.log_login_occurrence(user)
            session['login_occurrences'] = login_occurrences
            return redirect('/interests')
        else:
            crud.log_login_occurrence(user)
            return redirect('/')


@app.route('/interests')
def get_user_interests():
    """View get interests page."""

    if session.get('user_id'):
        all_interests_for_a_user = crud.get_all_interests_for_user(session['user_id'])
        session['log_in_occurrences'] = crud.get_user_login_occurrences(crud.get_user_by_id(session['user_id']))
        return render_template('get_user_interests.html', all_interests_for_a_user=all_interests_for_a_user)
    else:
        return redirect ("/")


def add_interest_to_db(interest):
    """Add interest to db."""

    # Check to see if interest already exist in db.
    interest_object = crud.get_interest_by_name(interest)
    if interest_object == None:
        interest_object = crud.create_interest(interest)

    return interest_object

def add_user_interest_to_db(user_id, interest):
    """Add userinterest to db"""

    # Check if userinterest is in database already;
    # If userinterest doesn't exist, create userinterest.
    user_interest = crud.get_user_interest(user_id, interest.interest_id)
    if user_interest == None:
        user_interest = crud.create_user_interest(user_id, interest.interest_id)
    else:
        pass

    return user_interest


@app.route('/handle-user-interests', methods=['POST'])
def handle_user_interests():
    """Handle user interests from form to add to db."""

    user_id = session['user_id']

    keywords = request.form.getlist('interests')

    for keyword in keywords:
        interest = add_interest_to_db(keyword)
        user_interest = add_user_interest_to_db(user_id, interest)

    return redirect('/')

@app.route('/read-books')
def show_read_books():
    """Show the books the user has read."""

    if session.get('user_id'):
        user = crud.get_user_by_id(session['user_id'])
        read_books = crud.get_read_books_by_user_id(session['user_id'])
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]
        return render_template('user_read_books.html', user=user, read_books=read_books, bookshelves=bookshelves)
    else:
        flash('Please log in to see your read books.')
        return redirect("/log-in")


@app.route('/liked-books')
def show_liked_books():
    """Show the books the user has liked."""

    if session.get('user_id'):
        user = crud.get_user_by_id(session['user_id'])
        liked_books = crud.get_liked_books_by_user_id(session['user_id'])
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]
        return render_template('user_liked_books.html', user=user, liked_books=liked_books, bookshelves=bookshelves)
    else:
        flash('Please log in to see your liked books.')
        return redirect("/log-in")


@app.route('/to-be-read-books')
def show_to_be_read_books():
    """Show the books the user has marked to be read."""

    if session.get('user_id'):
        user = crud.get_user_by_id(session['user_id'])
        to_be_read_books = crud.get_to_be_read_books_by_user_id(session['user_id'])
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]
        return render_template('user_to_be_read_books.html', user=user, to_be_read_books=to_be_read_books, bookshelves=bookshelves)
    else:
        flash('Please log in to see your tbr list.')
        return redirect("/log-in")


@app.route('/search-a-book')
def show_search_a_book():
    """Show results from user's book search."""
    if session.get('user_id'):
        search_result_and_keyword = google_books_api.search_a_book()
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]

        if search_result_and_keyword != None:
            return render_template('search_results.html', search_results=search_result_and_keyword[0], keyword=search_result_and_keyword[1], bookshelves=bookshelves)
        else:
            return redirect("/")
    else:
        flash('Please log in.')
        return redirect("/log-in")


def remove_illegal_characters_to_make_list(string):
    """Remove illegal characters from from strings to convert to a list."""

    illegal_characters = ["[", "]", "'"]

    valid_list = []
    if (string != "''") or (string != None):
        for letter in string:
            if letter in illegal_characters:
                continue
            else:
                valid_list.append(letter)
                valid_string = "".join(valid_list)
                valid_list = valid_string.split(",")
    else:
        valid_list = None

    return valid_list


def add_book_to_db(title, subtitle, description, image_link, isbn_13):
    """Add book to db."""

    # Check if the book is already in the database; If not in db, create book.
    book = crud.get_book_by_isbn_13(isbn_13)
    if book == None:
        book = crud.create_book(title, subtitle, description, image_link, isbn_13)
    else:
        pass

    return book

def add_book_to_library(book, user_id):
    """Add book to user library"""

    # Check if book is already in user library;
    # If not in user library, create bookinlibrary.
    book_in_library = crud.get_book_in_library(book, user_id)
    if book_in_library == None:
        book_in_library = crud.create_a_book_in_library(book, user_id)

    return book_in_library


def add_author_to_db(authors):
    """Add authors to db."""

    # Takes in authors as list
    # Check if author is in database;
    # If author doesn't exists, create author

    if authors != None:
        authors_in_db = []
        for author in authors:
            author_object = crud.get_author_by_full_name(author)
            if author_object == None:
                author_object = crud.create_author(author)
                authors_in_db.append(author_object)
            else:
                pass
    else:
        authors_in_db = None

    return authors_in_db


def add_book_author_to_db(book, authors_in_db):
    """Add bookauthor to db."""

    # Authors_in_db is a list
    # Check if bookauthor is in database;
    # If bookauthor doesn't exist, create bookauthor
    if authors_in_db != None:
        book_authors_in_db = []
        for author in authors_in_db:
            book_author_object = crud.get_book_author(book.book_id, author.author_id)
            if book_author_object == None:
                book_author_object = crud.create_book_author(book.book_id, author.author_id)

                book_authors_in_db.append(book_author_object)

    else:
        book_authors_in_db = None


    print(book_authors_in_db)

    return book_authors_in_db


def add_category_to_db(categories):
    """Add category to db."""

    # Categories as a list
    # Check if category is already in database;
    # If category doesn't exist, create category
    if categories != None:
        categories_in_db = []
        for category in categories:
            category_object = crud.get_category_by_name(category)
            if category_object == None:
                category_object = crud.create_category(category)
                categories_in_db.append(category_object)
            else:
                pass
    else:
        categories_in_db = None

    return categories_in_db


def add_book_category_to_db(book, categories_in_db):
    """Create new bookcategory in database."""

    # Categories_in_db is a list
    # Check if bookcategory is in database already;
    # If bookcategory doesn't exist, create bookcategory.
    if categories_in_db != None:
        book_categories_in_db = []
        for category in categories_in_db:
            book_category_object = crud.get_book_category(book.book_id, category.category_id)
            if book_category_object == None:
                book_category_object = crud.create_book_category(book.book_id, category.category_id)

                book_categories_in_db.append(book_category_object)
    else:
        book_categories_in_db = None

    return book_categories_in_db


def add_book_to_read_list(book_in_library):
    """Add book to user read list."""

    # Check if book is already on marked as a liked book for user
    # if so, flash message. If not mark as liked

    if book_in_library.read == True:
        message = '''You've already added this book to your Read Books'''
    else:
        read_status_update = True
        liked_status = False
        crud.mark_book_as_read(book_in_library, read_status_update, liked_status)
        message = 'Added to your Read Books'

    return message


def add_book_to_liked_list(book_in_library):
    """Add a bok to a user liked list."""

    if book_in_library.liked == True:
        read_status_update = True
        liked_status = False
        crud.remove_liked_tag(book_in_library, read_status_update, liked_status)
        message = 'Removed from your Liked Books'
    else:
        read_status_update = True
        liked_status = True
        crud.mark_book_as_liked(book_in_library, read_status_update, liked_status)
        message = 'Added to your Liked Books'

    return message

def add_book_to_to_be_read_list(book_in_library):
    """Add a book to a user liked list."""

    if book_in_library.to_be_read == True:
        message = 'This book is already on your TBR list.'
    else:
        read_status_update = False
        liked_status = False
        crud.mark_book_as_to_be_read(book_in_library, read_status_update, liked_status)
        message = 'Added to your TBR list'

    return message

def delete_book_from_read_list(isbn_13, user_id):
    """Remove book from user's read list."""

    book = crud.get_book_by_isbn_13(isbn_13)
    book_in_library = crud.get_book_in_library(book, user_id)
    crud.delete_book_from_library(book_in_library)


def remove_liked_tag(book_in_library):
    """Remove book as liked."""

    read_status_update = True
    liked_status = False
    crud.remove_liked_tag(book_in_library, read_status_update, liked_status)


def delete_book_from_to_be_read_list(isbn_13, user_id):
    """Remove book from user's read list."""

    book = crud.get_book_by_isbn_13(isbn_13)
    book_in_library = crud.get_book_in_library(book, user_id)
    crud.delete_book_from_library(book_in_library)


@app.route('/mark-as-read', methods=['POST'])
def mark_book_as_read():
    """Mark a book as read in a user library."""

    user_id = session['user_id']

    # get the title/subtitle/authors/image link/categories/description
    # from book user submitted as read
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    authors = request.form.get('authors', '')
    image_link = request.form.get('image_link')
    categories = request.form.get('categories', '')
    description = request.form.get('description')
    isbn_13 = request.form.get('isbn_13')

    authors_list = remove_illegal_characters_to_make_list(authors)
    categories_list = remove_illegal_characters_to_make_list(categories)

    book = add_book_to_db(title, subtitle, description, image_link, isbn_13)
    book_in_library = add_book_to_library(book, user_id)
    authors_in_db = add_author_to_db(authors_list)
    book_author = add_book_author_to_db(book, authors_in_db)
    categories_in_db = add_category_to_db(categories_list)
    book_category = add_book_category_to_db(book, categories_in_db)
    message = add_book_to_read_list(book_in_library)


    return message


@app.route('/mark-as-liked', methods=['POST'])
def mark_book_as_liked():
    """Mark a book as liked in a user library."""


    user_id = session['user_id']

    # get the title/subtitle/authors/image link/categories/description
    # from book user submitted as read
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    authors = request.form.get('authors', '')
    image_link = request.form.get('image_link')
    categories = request.form.get('categories', '')
    description = request.form.get('description')
    isbn_13 = request.form.get('isbn_13')

    authors_list = remove_illegal_characters_to_make_list(authors)
    categories_list = remove_illegal_characters_to_make_list(categories)

    book = add_book_to_db(title, subtitle, description, image_link, isbn_13)
    book_in_library = add_book_to_library(book, user_id)
    authors_in_db = add_author_to_db(authors_list)
    book_author = add_book_author_to_db(book, authors_in_db)
    categories_in_db = add_category_to_db(categories_list)
    book_category = add_book_category_to_db(book, categories_in_db)
    message = add_book_to_liked_list(book_in_library)

    for author in authors_list:
        interest = add_interest_to_db(author)
        user_interest = add_user_interest_to_db(user_id, interest)

    for category in categories_list:
        category = add_interest_to_db(category)
        user_interest = add_user_interest_to_db(user_id, category)

    return message


@app.route('/mark-as-to-be-read', methods=['POST'])
def mark_book_as_to_be_read():
    """Mark a book as liked in a user library."""

    user_id = session['user_id']

    # get the title/subtitle/authors/image link/categories/description
    # from book user submitted as read
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    authors = request.form.get('authors', '')
    image_link = request.form.get('image_link')
    categories = request.form.get('categories', '')
    description = request.form.get('description')
    isbn_13 = request.form.get('isbn_13')

    authors_list = remove_illegal_characters_to_make_list(authors)
    categories_list = remove_illegal_characters_to_make_list(categories)

    book = add_book_to_db(title, subtitle, description, image_link, isbn_13)
    book_in_library = add_book_to_library(book, user_id)
    authors_in_db = add_author_to_db(authors_list)
    book_author = add_book_author_to_db(book, authors_in_db)
    categories_in_db = add_category_to_db(categories_list)
    book_category = add_book_category_to_db(book, categories_in_db)
    message = add_book_to_to_be_read_list(book_in_library)

    return message


@app.route('/handle-remove-read-book' , methods=['POST'])
def remove_from_read_list():
    """Delete book from user read list."""

    user_id = session['user_id']
    isbn_13 = request.form.get('isbn_13')

    delete_book_from_read_list(isbn_13, user_id)

    return redirect('/read-books')


@app.route('/handle-remove-liked-book', methods=['POST'])
def remove_from_liked_list():
    """Delete from user liked lis.t"""

    user_id = session['user_id']
    isbn_13 = request.form.get('isbn_13')

    book = crud.get_book_by_isbn_13(isbn_13)
    book_in_library = crud.get_book_in_library(book, user_id)
    remove_liked_tag(book_in_library)

    return redirect('/liked-books')


@app.route('/handle-remove-to-be-read-book' , methods=['POST'])
def remove_from_to_be_read_list():
    """Delete book from user read list."""

    user_id = session['user_id']
    isbn_13 = request.form.get('isbn_13')

    delete_book_from_to_be_read_list(isbn_13, user_id)

    return redirect('/to-be-read-books')


@app.route('/handle-remove-book-on-bookshelf', methods=['POST'])
def remove_from_particular_bookshelf():
    """Remove book from a user's bookshelf."""

    user_id = session['user_id']
    isbn_13 = request.form.get('isbn_13')
    bookshelf_name = request.form.get('bookshelf_name')
    crud.remove_book_from_bookshelf(user_id, isbn_13, bookshelf_name)

    return redirect(f'/{bookshelf_name}-bookshelf')


@app.route('/handle-remove-interest', methods=['POST'])
def handle_removing_interest_from_user_profile():
    """Remove interest from technical profile."""

    user_id = session['user_id']
    interest = request.form.get('interest')

    crud.remove_interest(interest, user_id)

    return redirect('/interests')


@app.route('/create-bookshelf.json', methods=['POST'])
def create_bookshelf():
    """Create a bookshelf."""

    user_id = session['user_id']

    bookshelf_name = request.form.get('bookshelfName')

    bookshelf = crud.create_bookshelf(bookshelf_name, user_id)

    bookshelves_objects = crud.get_user_bookshelves(user_id)

    new_bookshelf = {'name': bookshelves_objects[-1].name}

    return jsonify(new_bookshelf)


@app.route('/<bookshelf_name>-bookshelf')
def show_bookshelf_details(bookshelf_name):

    bookshelf_name = bookshelf_name
    user_id = session['user_id']
    books_on_bookshelf = crud.get_all_books_on_a_bookshelf(bookshelf_name, user_id)

    return render_template('bookshelf_details.html', books_on_bookshelf=books_on_bookshelf, bookshelf_name=bookshelf_name)


def add_book_to_bookshelf(book_in_library, bookshelf):
    """Check to see if book_in_library is already on bookshelf and if not add it."""

    user_id = session['user_id']
    book_on_bookshelf = crud.get_book_on_bookshelf(book_in_library, bookshelf, user_id)
    print(f'its on the shelf already {book_on_bookshelf}')
    if book_on_bookshelf == None:
        date_added = datetime.now()
        book_on_bookshelf = crud.create_a_book_on_a_bookshelf(book_in_library, bookshelf, date_added)
    print(f'it has to be created on the shelf  {book_on_bookshelf}')
    return book_on_bookshelf


@app.route('/handle-adding-book-to-bookshelf', methods=['POST'])
def handle_adding_book_to_bookshelf():

    user_id = session['user_id']

    # get the book that will be added to bookshelf
    # get the shelf that will be added to bookshelf

    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    authors = request.form.get('authors')
    image_link = request.form.get('image_link')
    categories = request.form.get('categories')
    description = request.form.get('description')
    isbn_13 = request.form.get('isbn_13')
    bookshelf_name = request.form.get('bookshelf_name')
    book_tag = request.form.get('book_tag')

    authors_list = remove_illegal_characters_to_make_list(authors)
    categories_list = remove_illegal_characters_to_make_list(categories)

    book = add_book_to_db(title, subtitle, description, image_link, isbn_13)
    book_in_library = add_book_to_library(book, user_id)
    authors_in_db = add_author_to_db(authors_list)
    book_author = add_book_author_to_db(book, authors_in_db)
    categories_in_db = add_category_to_db(categories_list)
    book_category = add_book_category_to_db(book, categories_in_db)
    bookshelf = crud.get_a_bookshelf(user_id, bookshelf_name)
    book_on_bookshelf = add_book_to_bookshelf(book_in_library, bookshelf)

    if book_tag == 'read':
        add_book_to_read_list(book_in_library)
    elif book_tag == 'liked':
        add_book_to_liked_list(book_in_library)
    elif book_tag =='tbr':
        add_book_to_to_be_read_list(book_in_library)

    return f'Book added to {bookshelf_name} bookshelf.'

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)