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
# Mark between 2-15 of randomly selected books as read by user
gender_options = ['Female', 'Male', 'Non-binary', 'Prefer not to say']
for n in range(10):
    email = f'user{n+1}@test.com'
    password = f'testpassword{n+1}'
    full_name = fake.name()
    birthday = datetime.strptime(fake.date(), '%Y-%m-%d')
    gender = choice(gender_options)
    created_time = datetime.now() #strptime(fake.date(), '%Y-%m-%d')

    user = crud.create_user(email, password, full_name, birthday, gender, created_time)

    random_books = []
    for read_book in range(randint(2, 15)):
        random_book = choice(books_in_db)
        if random_book in random_books:
            continue
        else:
            random_books.append(random_book)

        crud.create_read_book_in_library(user, random_book, datetime.now(), read=True)






