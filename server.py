from flask import (Flask, render_template, request, flash, session,
                   redirect)

import requests

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

import os
from datetime import datetime

import json

app = Flask(__name__)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

app.secret_key = os.environ['FLASK_KEY']

API_KEY = os.environ['GOOGLEBOOKS_KEY']


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/sign-up')
def sign_up():
    """View sign up page."""

    return render_template('sign_up.html')


@app.route('/register', methods=['POST'])
def register_user():
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
        redirect_location='/sign-up'
    elif password != password_confirmed:
        flash('Passwords do not match.')
        redirect_location='/sign-up'
    else:
        crud.create_user(email, password, profile_name,
                        birthday, gender, time_created)
        flash('Account created! Please sign in.')
        redirect_location='/log-in'

    return redirect(redirect_location)


@app.route('/log-in')
def log_in():
    """User log in."""

    email = request.args.get('email')
    password = request.args.get('password')

    user = crud.get_user_by_email(email)


    if user == None or user.password != password:
        flash('The email and password you entered did not match our records. Please double-check and try again.')
    else:
        session['user_id'] = user.user_id
        user_id = session['user_id']
        session['profile_name'] = user.profile_name
        return redirect('user/{user_id}')

    return render_template('log_in.html')


@app.route('/user/<user_id>')
def show_user_details(user_id):
    """Show user details."""

    user_id = session['user_id']
    profile_name = session['profile_name']

    return render_template('user_details.html', user_id=user_id, profile_name=profile_name)


@app.route('/user/<user_id>/read-books')
def show_read_books(user_id):
    """Show the books the user has read."""


    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)

    read_books = crud.get_read_books_by_user_id(user_id)

    return render_template('user_read_books.html', user=user, read_books=read_books)


@app.route('/user/<user_id>/liked-books')
def show_liked_books(user_id):
    """Show the books the user has liked."""

    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)

    liked_books = crud.get_liked_books_by_user_id(user_id)

    return render_template('user_liked_books.html', user=user, liked_books=liked_books)


@app.route('/user/<user_id>/to-be-read-books')
def show_to_be_read_books(user_id):
    """Show the books the user has marked to be read."""

    user_id = session['user_id']

    user = crud.get_user_by_id(user_id)

    to_be_read_books = crud.get_to_be_read_books_by_user_id(user_id)

    return render_template('user_to_be_read_books.html', user=user, to_be_read_books=to_be_read_books)


@app.route('/search-a-book')
def search_a_book():
    """Show results from user's book search."""

    user_id = session['user_id']
    keyword = request.args.get('search', '')

    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'apikey': API_KEY, 'q': keyword, 'maxResults': 10}

    res = requests.get(url, params=payload)

    data = res.json()

    if keyword != '':

        search_results = []
        for n in range(len(data['items'])):

            search_result = {}

            base = data['items'][n]['volumeInfo']

            title = base['title']
            search_result['title'] = title

            subtitle = base.get('subtitle', None)
            if subtitle:
                search_result['subtitle'] = subtitle
            else:
                pass

            authors = base.get('authors', None)
            if authors:
                search_result['author'] = authors
            else:
                pass

            img_links = base.get('imageLinks', None)
            if img_links:
                thumbnail = img_links['thumbnail']
                search_result['thumbnail'] = thumbnail
            else:
                pass

            published_date = base.get('publishedDate', None)
            if published_date:
                search_result['published_date'] = published_date
            else:
                pass

            description = base.get('description', None)
            if description:
                search_result['description'] = description
            else:
                pass

            categories = base.get('categories', None)
            if categories:
                search_result['categories'] = categories
            else:
                pass

            search_results.append(search_result)

    else:
          return redirect('/user/<user_id>')

    return render_template('search_results.html', search_results=search_results, data=data)


def remove_illegal_characters(string):
    """Remove illegal characters from from data."""

    illegal_characters = ["[", "]", "'"]

    valid_list = []
    for letter in string:
        if letter in illegal_characters:
            continue
        else:
            valid_list.append(letter)
            authors = "".join(valid_list)

    return authors.split(",")


def add_book_to_db(title, subtitle, description, image_link):
    """Add book to db."""

    # check if the book is already in the database;
    # if not in db, create book
    book = crud.get_book_by_title(title)
    if book == None:
        book = crud.create_book(title, subtitle, description, image_link)
    else:
        pass

    return book

def add_book_to_library(book, user_id):
    """Add book to user library"""

    #check if book is already in user library;
    # if not in user library, create bookinlibrary

    book_in_library = crud.get_book_in_library(book, user_id)
    if book_in_library == None:
        book_in_library = crud.create_a_book_in_library(book, user_id)

    return book_in_library

def add_author_to_db(authors):
    """Add authors to db."""

    # takes in authors as list
    # check if author is in database;
    # if author doent exists, create author
    authors_in_db = []
    for author in authors:
        author_object = crud.get_author_by_full_name(author)
        if author_object == None:
            author_object = crud.create_author(author)
        else:
            pass

    authors_in_db.append(author_object)

    return authors_in_db


def add_book_author_to_db(book, authors_in_db):
    """Add bookauthor to db."""

    # authors_in_db is a list
    # check if bookauthor is in database;
    # if bookauthor doesn't exist, create bookauthor
    book_authors_in_db = []
    for author in authors_in_db:
        book_author_object = crud.get_book_author(book.book_id, author.author_id)
        if book_author_object == None:
            book_author_object = crud.create_book_author(book.book_id, author.author_id)
        else:
            pass

    book_authors_in_db.append(book_author_object)

    return book_authors_in_db


def add_category_to_db(categories):
    """Add category to db."""

    # categories is a list
    # check if category is already in database;
    # if category doesn't exist, create category
    categories_in_db = []
    for category in categories:
        category_object = crud.get_category_by_name(category)
        if category_object == None:
            category_object = crud.create_category(category)
        else:
            pass

    categories_in_db.append(category_object)

    return categories_in_db


def add_book_category_to_db(book, categories_in_db):
    """Create new bookcategory in database."""

    # categories_in_db is a list
    # check if bookcategory is in database;
    # if bookcategory doesn't exist, create bookcategory.
    book_categories_in_db = []
    for category in categories_in_db:
        book_category_object = crud.get_book_category(book.book_id, category.category_id)
        if book_category_object == None:
            book_category_object = crud.create_book_category(book.book_id, category.category_id)

    book_categories_in_db.append(book_category_object)

    return book_categories_in_db


def add_book_to_read_list(book_in_library, user_id):
    """Add book to user read list."""

    # # see if book is in library
    # read_book_in_collection = crud.get_book_in_library(book, user_id)
    #if so check to see if already read and if read then flash message
    # if read_book_in_collection:
    if book_in_library.read == True:
        flash('This book is already on your read list.')
    else:
        crud.mark_book_in_library_as_read(book_in_library, user_id)
        flash('Book Added!')


    print("=====================================")
    print("=====================================")
    print("=====================================")
    print("=====================================")
    print(book_in_library)
    print(book_in_library.read)
    print(type(book_in_library))
    print("=====================================")
    print("=====================================")
    # # see if book is already in user's read books collection
    # read_book_in_in_collection = crud.get_read_book_by_title(book.title, user_id)
    # # if so, flash a message.
    # if read_book_in_in_collection:
    #     flash('This book is already on your read list.')
    # # Otherwise, add book as read in user's library and flash message
    # else:
    #     book_id = book.book_id
    #     read = True
    #     read_date = datetime.now()
    #     read_book_in_in_collection = crud.create_read_book(user_id, book_id, read, read_date)
    #     flash('Book Added!')

def add_book_to_liked_list(book, user_id):
    """Add a bok to a user liked list"""

    # See if book is in user's read books collection
    # if not, do not like
    read_book_in_in_collection = crud.get_read_book_by_title(book.title, user_id)
    if read_book_in_in_collection == None:
        flash('''Looks like you haven't read this book yet.''')
        liked_book_in_collection = None
    else:
    # See if book is already in user's liked books collection
        liked_book_in_collection = crud.get_liked_book_by_title(book.title, user_id)
        if liked_book_in_collection:
            flash('You have already liked this book.')
        else:
            book_id = book.book_id
            liked = True
            liked_date = datetime.now()
            liked_book_in_collection = crud.create_liked_book(user_id, book_id, liked, liked_date)
            flash('Book liked!')

# def add_book_to_read_list(book, user_id):
#     """Add book to user read list."""

#     # see if book is already in user's read books collection
#     read_book_in_in_collection = crud.get_read_book_by_title(book.title, user_id)
#     # if so, flash a message.
#     if read_book_in_in_collection:
#         flash('This book is already on your read list.')
#     # Otherwise, add book as read in user's library and flash message
#     else:
#         book_id = book.book_id
#         read = True
#         liked = False
#         liked_date = None
#         to_be_read = False
#         to_be_read_date = None
#         read_date = datetime.now()
#         read_book_in_in_collection = crud.create_a_book_in_library(user_id, book_id, read, read_date,
#                                                           liked, liked_date, to_be_read,
#                                                           to_be_read_date)
#         flash('Book Added!')




@app.route('/mark-as-read')
def mark_book_as_read():
    """Mark a book as read in a user library."""

    user_id = session['user_id']

    # get the title/subtitle/authors/image link/categories/description
    # from book user submitted as read
    title = request.args.get('title')
    subtitle = request.args.get('subtitle')
    authors = request.args.get('authors')
    image_link = request.args.get('image_link')
    categories = request.args.get('categories')
    description = request.args.get('description')

    sanitized_authors_list = remove_illegal_characters(authors)
    sanitized_categories_list = remove_illegal_characters(categories)

    book = add_book_to_db(title, subtitle, description, image_link)
    book_in_library = add_book_to_library(book, user_id)
    authors_in_db = add_author_to_db(sanitized_authors_list)
    book_author = add_book_author_to_db(book, authors_in_db)
    categories_in_db = add_category_to_db(sanitized_categories_list)
    book_category = add_book_category_to_db(book, categories_in_db)
    read_book_in_collection = add_book_to_read_list(book_in_library, user_id)

    return redirect('/user/<user_id>/read-books')

@app.route('/mark-as-liked')
def mark_book_as_liked():
    """Mark a book as liked in a user library"""


    user_id = session['user_id']

    # get the title/subtitle/authors/image link/categories/description
    # from book user submitted as read
    title = request.args.get('title')
    subtitle = request.args.get('subtitle')
    authors = request.args.get('authors')
    image_link = request.args.get('image_link')
    categories = request.args.get('categories')
    description = request.args.get('description')

    sanitized_authors_list = remove_illegal_characters(authors)
    sanitized_categories_list = remove_illegal_characters(categories)

    book = add_book_to_db(title, subtitle, description, image_link)
    authors_in_db = add_author_to_db(sanitized_authors_list)
    book_author = add_book_author_to_db(book, authors_in_db)
    categories_in_db = add_category_to_db(sanitized_categories_list)
    book_category = add_book_category_to_db(book, categories_in_db)
    liked_book_in_collection = add_book_to_liked_list(book, user_id)

    return redirect('/user/<user_id>/liked-books')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)