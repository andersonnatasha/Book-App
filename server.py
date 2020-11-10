from flask import (Flask, render_template, request, flash, session,
                   redirect)

import requests

from model import connect_to_db
import crud

from jinja2 import StrictUndefined

import os
from datetime import datetime

app = Flask(__name__)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

app.secret_key = os.environ['FLASK_KEY']

API_KEY = os.environ['GOOGLEBOOKS_KEY']


@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route('/sign-up')
def sign_up():
    """View sign up page"""

    return render_template('sign_up.html')


@app.route('/register', methods=['POST'])
def register_user():
    """Register a user"""

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
    """User log in"""

    email = request.args.get('email')
    password = request.args.get('password')

    user = crud.get_user_by_email(email)


    if user == None or user.password != password:
        flash('The email and password you entered did not match our records. Please double-check and try again.')
    else:
        session['user_id'] = user.user_id
        return redirect('/user/<user_id>')

    return render_template('log_in.html')


@app.route('/user/<user_id>')
def show_user_details(user_id):
    """Show user details"""

    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

@app.route('/user/<user_id>/read-books')
def show_read_books(user_id):
    """Show the books the user has read"""


    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)

    read_books = crud.get_read_books_by_user_id(user_id)


    return render_template('user_read_books.html', user=user, read_books=read_books)

@app.route('/user/<user_id>/liked-books')
def show_liked_books(user_id):
    """Show the books the user has liked"""

    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)

    liked_books = crud.get_liked_books_by_user_id(user_id)


    return render_template('user_liked_books.html', user=user, liked_books=liked_books)


@app.route('/user/<user_id>/to-be-read-books')
def show_to_be_read_books(user_id):
    """Show the books the user has marked to be read"""

    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)

    to_be_read_books = crud.get_to_be_read_books_by_user_id(user_id)

    return render_template('user_to_be_read_books.html', user=user, to_be_read_books=to_be_read_books)

@app.route('/search-a-book')
def search_a_book():
    """Show results from user's book search"""

    user_id = session['user_id']
    keyword = request.args.get('search', '')

    url = 'https://www.googleapis.com/books/v1/volumes'
    payload = {'apikey': API_KEY, 'q': keyword, 'maxResults': 10}

    res = requests.get(url, params=payload)

    data = res.json()

    search_results = []

    for n in range(len(data['items'])):
        print(f"---------{n}-------------")

        base = data['items'][n]['volumeInfo']

        title = base['title']
        search = {'title':title}
        search_results.append(search)

        subtitle= base.get('subtitle', None)
        if subtitle:
            subtitle = base['subtitle']
            search_results[n]['subtitle'] = subtitle
        else:
            pass

        authors = base['authors']
        search_results[n]['author'] = authors

        img_links = base.get('imageLinks', None)
        if img_links:
            thumbnail = img_links['thumbnail']
            search_results[n]['thumbnail'] = thumbnail
        else:
            pass

        published_date = base['publishedDate']
        search_results[n]['published_date'] = published_date

    return render_template('search_results.html', search_results=search_results)





if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)