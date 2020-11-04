"""Models for book app."""

from flask_sqlalchemy import SQLAlchemy

db = SQAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'