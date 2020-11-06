from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

