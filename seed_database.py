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