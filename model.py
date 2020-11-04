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