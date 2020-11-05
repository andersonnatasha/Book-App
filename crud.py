"""CRUD operations"""

from model import db, User, Book, BookCopy, Author, Category, BookCategory, connect_to_db



if __name == '__main__':
    from server import app
    connect_to_db(app)
    