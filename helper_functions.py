from flask import request, session
import os
import requests
import crud
from random import randint
from random import choice
from datetime import datetime

API_KEY = os.environ['GOOGLEBOOKS_KEY']


def search_a_book():
    """Show results from user's book search."""

    keyword = request.args.get('search', '')

    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'q': keyword, 'maxResults': 10, 'apikey': API_KEY}

    res = requests.get(url, params=payload)

    data = res.json()

    search_results = []

    if keyword != '':

        for n in range(len(data['items'])):

            search_result = {}

            base = data['items'][n]['volumeInfo']
            search_result['isbn_13'] = None

            if base.get('industryIdentifiers', None) and (base['industryIdentifiers'][-1]['type'] == 'ISBN_13') and (base.get('imageLinks')):
                search_result['isbn_13'] = base['industryIdentifiers'][-1]['identifier']

            elif base.get('industryIdentifiers', None) and (base['industryIdentifiers'][0]['type'] == 'ISBN_13') and (base.get('imageLinks')):
                search_result['isbn_13'] = base['industryIdentifiers'][0]['identifier']

            if search_result['isbn_13'] != None:

                keys_to_search_for_in_data = [
                    'title', 'subtitle', 'authors', 'publishedDate', 'description', 'categories']

                for key in keys_to_search_for_in_data:
                    if key in base:
                        search_result[key] = base[key]

                    search_result['thumbnail'] = base['imageLinks']['thumbnail']

                search_results.append(search_result)

    if keyword != "":
        search_result_and_keyword = [search_results, keyword]
    else:
        search_result_and_keyword = None

    return search_result_and_keyword


def show_recommended_books(interest):
    """show recommended books."""

    user_id = session['user_id']
    # keywords = crud.get_all_interests_for_user(user_id)

    search_results = []
    # for keyword in keywords:
    # keyword = keyword.interest
    url = 'https://www.googleapis.com/books/v1/volumes'
    keyword = f'subject:{interest}'
    # randint_high = 1000
    payload = {'q': keyword, 'maxResults': 15, 'apikey': API_KEY}
    # payload = {'q': keyword, 'maxResults': 15,
    #            'startIndex': randint(0, randint_high), 'apikey': API_KEY}

    res = requests.get(url, params=payload)

    data = res.json()
    print("?????????????????????????????????????????????????????")
    print("?????????????????????????????????????????????????????")
    print("?????????????????????????????????????????????????????")
    print(payload)
    print("?????????????????????????????????????????????????????")
    print("?????????????????????????????????????????????????????")
    print("?????????????????????????????????????????????????????")

    # while not data.get('items'):
    #     randint_high -= 50
    #     payload = {'q': keyword, 'maxResults': 10, 'startIndex': randint(
    #         0, randint_high), 'apikey': API_KEY}
    #     res = requests.get(url, params=payload)
    #     data = res.json()

    for n in range(len(data['items'])):

        search_result = {}

        base = data['items'][n]['volumeInfo']
        search_result['isbn_13'] = None

        if base.get('industryIdentifiers', None) and (base['industryIdentifiers'][-1]['type'] == 'ISBN_13') and (base.get('imageLinks')):
            search_result['isbn_13'] = base['industryIdentifiers'][-1]['identifier']

        elif base.get('industryIdentifiers', None) and (base['industryIdentifiers'][0]['type'] == 'ISBN_13') and (base.get('imageLinks')):
            search_result['isbn_13'] = base['industryIdentifiers'][0]['identifier']

        if search_result['isbn_13'] != None:

            keys_to_search_for_in_data = [
                'title', 'subtitle', 'authors', 'publishedDate', 'description', 'categories']

            for key in keys_to_search_for_in_data:
                if key in base:
                    search_result[key] = base[key]

            if base.get('imageLinks'):
                search_result['thumbnail'] = base['imageLinks']['thumbnail']

            search_results.append(search_result)

    return search_results


def choose_random_quote():
    quotes = ['''Reading is an act of civilization; it’s one of the greatest
        acts of civilization because it takes the free raw material of the
        mind and builds castles of possibilities. —Ben Okri''',
              '''Reading is a discount ticket to everywhere. —Mary Schmich''',
              '''We read in bed because reading is halfway between life and dreaming,
        our own consciousness in someone else’s mind. —Anna Quindlen''',
              '''It’s no use of talking unless people understand what you say.” -Zora Neale Hurston''',
              '''“We write for the same reason that we walk, talk, climb mountains or swim the oceans –
        because we can. We have some impulse within us that makes us want to explain ourselves to
        other human beings.” – Maya Angelou''',
              '''“If there’s a book you really want to read, but it hasn’t been written yet,
        then you must write it.” -Toni Morrison''',
              '''“The ability of writers to imagine what is not the self,
        to familiarize the strange and mystify the familiar, is the test of their power.” -Toni Morrison''',
              '''“Many stories matter. Stories have been used to dispossess and to malign. But stories can also be
        used to empower, and to humanize. Stories can break the dignity of a people. But stories can also repair
        that broken dignity.” ― Chimamanda Ngozi Adichie''',
              '''“Poetry is a political act because it involves telling the truth.” ― June Jordan''']

    return choice(quotes)


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
        user_interest = crud.create_user_interest(
            user_id, interest.interest_id)

    return user_interest


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
        book = crud.create_book(
            title, subtitle, description, image_link, isbn_13)

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
                authors_in_db.append(author_object)
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
            book_author_object = crud.get_book_author(
                book.book_id, author.author_id)
            if book_author_object == None:
                book_author_object = crud.create_book_author(
                    book.book_id, author.author_id)

                book_authors_in_db.append(book_author_object)

    else:
        book_authors_in_db = None

    return book_authors_in_db


def add_category_to_db(category):
    """Add category to db."""

    # Categories as a list - not anymore
    # Check if category is already in database;
    # If category doesn't exist, create category
    # if categories != None:
    categories_in_db = []
    # for category in categories:
    category_object = crud.get_category_by_name(category)
    if category_object == None:
        category_object = crud.create_category(category)
        categories_in_db.append(category_object)

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
            book_category_object = crud.get_book_category(
                book.book_id, category.category_id)
            if book_category_object == None:
                book_category_object = crud.create_book_category(
                    book.book_id, category.category_id)

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
        crud.mark_book_as_read(
            book_in_library, read_status_update, liked_status)
        message = 'Added to your Read Books'

    return message


def add_book_to_liked_list(book_in_library):
    """Add a bok to a user liked list."""

    if book_in_library.liked == True:
        read_status_update = True
        liked_status = False
        crud.remove_liked_tag(
            book_in_library, read_status_update, liked_status)
        message = 'Removed from your Liked Books'
    else:
        read_status_update = True
        liked_status = True
        crud.mark_book_as_liked(
            book_in_library, read_status_update, liked_status)
        message = 'Added to your Liked Books'

    return message


def add_book_to_to_be_read_list(book_in_library):
    """Add a book to a user liked list."""

    if book_in_library.to_be_read == True:
        message = 'This book is already on your TBR list.'
    else:
        read_status_update = False
        liked_status = False
        crud.mark_book_as_to_be_read(
            book_in_library, read_status_update, liked_status)
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


def add_book_to_bookshelf(book_in_library, bookshelf):
    """Check to see if book_in_library is already on bookshelf and if not add it."""

    user_id = session['user_id']
    book_on_bookshelf = crud.get_book_on_bookshelf(
        book_in_library, bookshelf, user_id)
    print(f'its on the shelf already {book_on_bookshelf}')
    if book_on_bookshelf == None:
        date_added = datetime.now()
        book_on_bookshelf = crud.create_a_book_on_a_bookshelf(
            book_in_library, bookshelf, date_added)
    print(f'it has to be created on the shelf  {book_on_bookshelf}')

    return book_on_bookshelf


def add_recommended_books_to_db(interest):
    """Given an interest add 20 books to the database."""

    user_id = session['user_id']
    search_results = show_recommended_books(interest)
    print("?????????????????????????????/")
    print("?????????????????????????????/")
    print("?????????????????????????????/")
    print(search_results)

    for search_result in search_results:
        book = add_book_to_db(
            search_result.get('title'), search_result.get('subtitle'),
            search_result.get('description'), search_result.get('thumbnail'),
            search_result.get('isbn_13'))
        if search_result.get('authors'):
            authors_list = remove_illegal_characters_to_make_list(
                search_result['authors'])
            authors_in_db = add_author_to_db(authors_list)
            add_book_author_to_db(book, authors_in_db)
        if search_result.get('categories'):
            categories_list = remove_illegal_characters_to_make_list(
                search_result['categories'])
            for category in categories_list:
                if category == interest:
                    categories_in_db = add_category_to_db(category)
                    add_book_category_to_db(book, categories_in_db)
                    crud.create_recommended_book(book.book_id, user_id)
