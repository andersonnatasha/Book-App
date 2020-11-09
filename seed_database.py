"""Script to seed database"""

import os
import json
from datetime import datetime
from random import choice
from random import randint
from faker import Faker


import crud
import model
import server

os.system('dropdb bookslibrary')
os.system('createdb bookslibrary')

model.connect_to_db(server.app)
model.db.create_all()

fake = Faker()


# Create 30 books
books_in_db = []
for n in range(30):
    title = f'title{n+1}'
    description = fake.paragraph(nb_sentences=5)

    db_book = crud.create_book(title, description)
    books_in_db.append(db_book)

# Create one author for each book
for n in range(len(books_in_db)):
    fname = fake.first_name()
    lname = fake.last_name()
    book = books_in_db[n]

    crud.create_author(fname, lname, book)

# Create 50 categories
# and assign one BookCategory to a book/category
categories_in_db = []
for n in range(40):
    category = f'category{n+1}'

    db_category = crud.create_category(category)
    categories_in_db.append(db_category)

for n in range(len(books_in_db)):
    book = books_in_db[n]
    random_category = choice(categories_in_db)

    crud.create_book_category(book, random_category)


# Create 10 users with unique emails
gender_options = ['Female', 'Male', 'Non-binary', 'Prefer not to say']
for n in range(10):
    email = f'user{n+1}@test.com'
    password = f'testpassword{n+1}'
    full_name = fake.name()
    birthday = datetime.strptime(fake.date(), '%Y-%m-%d')
    gender = choice(gender_options)
    created_time = datetime.now()  # strptime(fake.date(), '%Y-%m-%d')

    user = crud.create_user(email, password, full_name,
                            birthday, gender, created_time)

# Mark between 1-7 of randomly selected books as read by user
# and assign boolean value for if book is liked.
    liked_options = [True, False]
    read_options = [True, False]
    books_in_library = []

    for book in range(randint(1, 7)):
        books_in_db = books_in_db
        book = choice(books_in_db)
        read = choice(read_options)

        if book not in books_in_library:
            if read == True:
                to_be_read = False
                to_be_read_date = None
                read_date = datetime.strptime(fake.date(), '%Y-%m-%d')
                liked = choice(liked_options)
                if liked == True:
                    liked_date = datetime.strptime(fake.date(), '%Y-%m-%d')
                else:
                    liked_date = None
            else:
                to_be_read = True
                to_be_read_date = datetime.strptime(fake.date(), '%Y-%m-%d')
                read_date = None
                read = False
                read_date = None
                liked = False
                liked_date = None


            books_in_db.append(book)

        else:
            continue

        crud.create_a_book_in_library(user, book, read, read_date, liked,
                                        liked_date, to_be_read, to_be_read_date)
