"""Models for book app."""

from flask_sqlalchemy import SQLAlchemy

db = SQAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True
                        )
    full_name = db.Column(db.String(50),
                          nullable=False)
    email = db.Column(db.String(50),
                     nullable=False)
    gender = db.Column(db.String(17))
    created_at = db.Column(db.DateTime)

class ReadBooksShelf(db.Model):
    """A bookshelf of read books."""