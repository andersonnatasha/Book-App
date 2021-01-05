from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)

from model import connect_to_db

import crud

import helper_functions

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

        search_results = crud.get_recommended_books(user_id)
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]
        return render_template('homepage.html', search_results=search_results, bookshelves=bookshelves)
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

    birthday = datetime.strptime(
        f'{birth_month}/{birth_day}/{birth_year}', ('%B/%d/%Y'))

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
    quote = helper_functions.choose_random_quote()
    return render_template('log_in.html', quote=quote)


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
        all_interests_for_a_user = crud.get_all_interests_for_user(
            session['user_id'])
        session['log_in_occurrences'] = crud.get_user_login_occurrences(
            crud.get_user_by_id(session['user_id']))
        quote = helper_functions.choose_random_quote()
        return render_template('get_user_interests.html', all_interests_for_a_user=all_interests_for_a_user, quote=quote)
    else:
        return redirect("/")


@app.route('/handle-user-interests', methods=['POST'])
def handle_user_interests():
    """Handle user interests from form to add to db."""

    user_id = session['user_id']

    keywords = request.form.getlist('interests')

    for keyword in keywords:
        interest = helper_functions.add_interest_to_db(keyword)
        helper_functions.add_user_interest_to_db(user_id, interest)
        helper_functions.add_recommended_books_to_db_by_category(
            interest.interest)

    return redirect('/')


@app.route('/add-more-recommended_books', methods=['POST'])
def add_more_recommended_books():
    """add more recommended books to db based on user interests"""

    interests = crud.get_all_interests_for_user(session['user_id'])
    for interest in interests:
        helper_functions.add_recommended_books_to_db_by_category(
            interest.interest.interest)
        print(">>>>>>>>>>>>>>??????")
        print(interest.interest.interest)

    return redirect("/")


@app.route('/handle-remove-interest', methods=['POST'])
def handle_removing_interest_from_user_profile():
    """Remove interest from technical profile."""

    user_id = session['user_id']
    interest = request.form.get('interest')

    crud.remove_interest(interest, user_id)
    crud.remove_all_recommended_books_of_a_particular_interest(
        user_id, interest)

    return redirect('/interests')


@app.route('/read-books')
def show_read_books():
    """Show the books the user has read."""

    if session.get('user_id'):
        user = crud.get_user_by_id(session['user_id'])
        read_books = crud.get_read_books_by_user_id(session['user_id'])
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]
        quote = helper_functions.choose_random_quote()
        return render_template('user_read_books.html', user=user, read_books=read_books, bookshelves=bookshelves, quote=quote)
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
        quote = helper_functions.choose_random_quote()
        return render_template('user_liked_books.html', user=user, liked_books=liked_books, bookshelves=bookshelves, quote=quote)
    else:
        flash('Please log in to see your liked books.')
        return redirect("/log-in")


@app.route('/to-be-read-books')
def show_to_be_read_books():
    """Show the books the user has marked to be read."""

    if session.get('user_id'):
        user = crud.get_user_by_id(session['user_id'])
        to_be_read_books = crud.get_to_be_read_books_by_user_id(
            session['user_id'])
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]
        quote = helper_functions.choose_random_quote()
        return render_template('user_to_be_read_books.html', user=user, to_be_read_books=to_be_read_books, bookshelves=bookshelves, quote=quote)
    else:
        flash('Please log in to see your tbr list.')
        return redirect("/log-in")


@app.route('/search-a-book')
def show_search_a_book():
    """Show results from user's book search."""
    if session.get('user_id'):
        search_result_and_keyword = helper_functions.search_a_book()
        bookshelves = crud.get_user_bookshelves(session['user_id'])
        bookshelves = bookshelves[::-1]
        quote = helper_functions.choose_random_quote()
        if search_result_and_keyword != None:
            return render_template('search_results.html', search_results=search_result_and_keyword[0], keyword=search_result_and_keyword[1], bookshelves=bookshelves, quote=quote)
        else:
            return redirect("/")
    else:
        flash('Please log in.')
        return redirect("/log-in")


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

    authors_list = helper_functions.remove_illegal_characters_to_make_list(
        authors)
    categories_list = helper_functions.remove_illegal_characters_to_make_list(
        categories)

    book = helper_functions.add_book_to_db(
        title, subtitle, description, image_link, isbn_13)
    book_in_library = helper_functions.add_book_to_library(book, user_id)
    for author in authors_list:
        authors_in_db = helper_functions.add_author_to_db(author)
        helper_functions.add_book_author_to_db(book, authors_in_db)

    for category in categories_list:
        category_in_db = helper_functions.add_category_to_db(category)
        helper_functions.add_book_category_to_db(book, category_in_db)
    message = helper_functions.add_book_to_read_list(book_in_library)

    return message


@app.route('/mark-as-liked', methods=['POST'])
def mark_book_as_liked():
    """Mark a book as liked in a user library."""

    user_id = session['user_id']

    # get the title/subtitle/authors/image link/categories/description
    # from book user submitted as read
    title = request.form.get('title', '')
    subtitle = request.form.get('subtitle', '')
    authors = request.form.get('authors', '')
    image_link = request.form.get('image_link', '')
    categories = request.form.get('categories', '')
    description = request.form.get('description', '')
    isbn_13 = request.form.get('isbn_13', '')

    authors_list = helper_functions.remove_illegal_characters_to_make_list(
        authors)
    categories_list = helper_functions.remove_illegal_characters_to_make_list(
        categories)

    book = helper_functions.add_book_to_db(
        title, subtitle, description, image_link, isbn_13)
    book_in_library = helper_functions.add_book_to_library(book, user_id)
    for author in authors_list:
        authors_in_db = helper_functions.add_author_to_db(author)
        helper_functions.add_book_author_to_db(book, authors_in_db)
        interest = helper_functions.add_interest_to_db(author)
        helper_functions.add_user_interest_to_db(user_id, interest)

    for category in categories_list:
        category_in_db = helper_functions.add_category_to_db(category)
        helper_functions.add_book_category_to_db(book, category_in_db)
        category = helper_functions.add_interest_to_db(category)
        helper_functions.add_user_interest_to_db(user_id, category)
        helper_functions.add_recommended_books_to_db_by_category(
            category.interest)
    message = helper_functions.add_book_to_liked_list(book_in_library)

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

    book = helper_functions.add_book_to_db(
        title, subtitle, description, image_link, isbn_13)
    book_in_library = helper_functions.add_book_to_library(book, user_id)

    authors_list = helper_functions.remove_illegal_characters_to_make_list(
        authors)
    for author in authors_list:
        authors_in_db = helper_functions.add_author_to_db(author)
        helper_functions.add_book_author_to_db(book, authors_in_db)

    categories_list = helper_functions.remove_illegal_characters_to_make_list(
        categories)
    for category in categories_list:
        category_in_db = helper_functions.add_category_to_db(category)
        helper_functions.add_book_category_to_db(book, category_in_db)
    message = helper_functions.add_book_to_to_be_read_list(book_in_library)

    return message


@app.route('/handle-remove-read-book', methods=['POST'])
def remove_from_read_list():
    """Delete book from user read list."""

    user_id = session['user_id']
    isbn_13 = request.form.get('isbn_13')

    helper_functions.delete_book_from_read_list(isbn_13, user_id)

    return redirect('/read-books')


@app.route('/handle-remove-liked-book', methods=['POST'])
def remove_from_liked_list():
    """Delete from user liked lis.t"""

    user_id = session['user_id']
    isbn_13 = request.form.get('isbn_13')

    book = crud.get_book_by_isbn_13(isbn_13)
    book_in_library = crud.get_book_in_library(book, user_id)
    helper_functions.remove_liked_tag(book_in_library)

    return redirect('/liked-books')


@app.route('/handle-remove-to-be-read-book', methods=['POST'])
def remove_from_to_be_read_list():
    """Delete book from user read list."""

    user_id = session['user_id']
    isbn_13 = request.form.get('isbn_13')

    helper_functions.delete_book_from_to_be_read_list(isbn_13, user_id)

    return redirect('/to-be-read-books')


@app.route('/handle-remove-book-on-bookshelf', methods=['POST'])
def remove_from_particular_bookshelf():
    """Remove book from a user's bookshelf."""

    user_id = session['user_id']
    isbn_13 = request.form.get('isbn_13')
    bookshelf_name = request.form.get('bookshelf_name')
    crud.remove_book_from_bookshelf(user_id, isbn_13, bookshelf_name)

    return redirect(f'/{bookshelf_name}-bookshelf')


@app.route('/create-bookshelf.json', methods=['POST'])
def create_bookshelf():
    """Create a bookshelf."""

    user_id = session['user_id']

    bookshelf_name = request.form.get('bookshelfName')

    crud.create_bookshelf(bookshelf_name, user_id)

    bookshelves_objects = crud.get_user_bookshelves(user_id)

    new_bookshelf = {'name': bookshelves_objects[-1].name}

    return jsonify(new_bookshelf)


@app.route('/<bookshelf_name>-bookshelf')
def show_bookshelf_details(bookshelf_name):

    bookshelf_name = bookshelf_name
    user_id = session['user_id']
    books_on_bookshelf = crud.get_all_books_on_a_bookshelf(
        bookshelf_name, user_id)
    bookshelves = crud.get_user_bookshelves(session['user_id'])
    bookshelves = bookshelves[::-1]
    quote = helper_functions.choose_random_quote()

    return render_template('bookshelf_details.html', books_on_bookshelf=books_on_bookshelf, bookshelf_name=bookshelf_name, bookshelves=bookshelves, quote=quote)


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

    authors_list = helper_functions.remove_illegal_characters_to_make_list(
        authors)
    categories_list = helper_functions.remove_illegal_characters_to_make_list(
        categories)

    book = helper_functions.add_book_to_db(
        title, subtitle, description, image_link, isbn_13)
    book_in_library = helper_functions.add_book_to_library(book, user_id)
    for author in authors_list:
        authors_in_db = helper_functions.add_author_to_db(author)
        helper_functions.add_book_author_to_db(book, authors_in_db)

    for category in categories_list:
        category_in_db = helper_functions.add_category_to_db(category)
        helper_functions.add_book_category_to_db(book, category_in_db)
    bookshelf = crud.get_a_bookshelf(user_id, bookshelf_name)
    helper_functions.add_book_to_bookshelf(book_in_library, bookshelf)

    if book_tag == 'Read':
        helper_functions.add_book_to_read_list(book_in_library)
    elif book_tag == 'Liked':
        helper_functions.add_book_to_liked_list(book_in_library)
    elif book_tag == 'TBR':
        helper_functions.add_book_to_to_be_read_list(book_in_library)

    return f'Book added to {bookshelf_name} bookshelf.'


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
