from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

import os

app = Flask(__name__)
app.secrect_key = os.environ['FLASK_KEY']


@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')

@app.route('/sign-up')
def sign_up():
    """Register a user"""

    return render_template('sign_up.html')

@app.route('/log-in')
def login():
    """user log in"""

    return render_template('log_in.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)