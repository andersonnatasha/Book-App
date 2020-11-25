"""Script to seed database."""

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
    title = f'Title {n+1}'
    image_link = fake.sentence()
    subtitle = f'Subtitle {n+1}'
    description = fake.paragraph(nb_sentences=5)
    isbn_13 = '1234567891234'

    db_book = crud.create_book(title, subtitle, description, image_link, isbn_13)
    books_in_db.append(db_book)

# Create either one or two author for each book
for n in range(len(books_in_db)):
    for author in range(randint(1, 2)):
        full_name = fake.name()
        book = books_in_db[n]

        crud.create_author(full_name)

#Create 50 categories
#and assign one BookCategory to a book/category
categories_in_db = []
for n in range(40):
    category = f'category {n+1}'

    db_category = crud.create_category(category)
    categories_in_db.append(db_category)


# for n in range(len(books_in_db)):
#     book = books_in_db[n]
#     random_category = choice(categories_in_db)

#     crud.create_book_category(book, random_category)

print(categories_in_db)


# Create 10 users with unique emails
gender_options = ['Female', 'Male', 'Non-binary', 'Prefer not to say']
for n in range(10):
    email = f'user{n+1}@test.com'
    password = f'testpassword{n+1}'
    profile_name = fake.name()
    birthday = datetime.strptime(fake.date(), '%Y-%m-%d')
    gender = choice(gender_options)
    time_created  = datetime.now()

    user = crud.create_user(email, password, profile_name,
                            birthday, gender, time_created)


# Create 30 interests and assign





# Mark between 5-30 of randomly selected books as read by user

    # books_in_library = set()
    # for book in range(randint(5, 30)):
    #     liked_options = [True, False]
    #     read_options = [True, False]

    #     books_in_db = set(books_in_db)
    #     books_not_in_library = books_in_db - books_in_library
    #     list_books_not_in_library = list(books_not_in_library)

    #     book = choice(list_books_not_in_library)
    #     read = choice(read_options)

    #     if read == True:
    #         to_be_read = False
    #         to_be_read_date = None
    #         read_date = datetime.strptime(fake.date(), '%Y-%m-%d')
    #         liked = choice(liked_options)
    #         if liked == True:
    #             liked_date = datetime.strptime(fake.date(), '%Y-%m-%d')
    #         else:
    #             liked_date = None
    #     else:
    #         to_be_read = True
    #         to_be_read_date = datetime.strptime(fake.date(), '%Y-%m-%d')
    #         read = False
    #         read_date = None
    #         liked = False
    #         liked_date = None

    #     books_in_library.add(book)

    #     crud.create_a_book_in_library(user, book, read, read_date, liked,
    #                                     liked_date, to_be_read, to_be_read_date)
