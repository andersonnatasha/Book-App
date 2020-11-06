"""Script to seed database"""

import os 
import json 
from datetime import datetime
from faker import Faker

import crud
import model
import server

os.system('dropdb bookslibrary')
os.system('createdb bookslibrary')

model.connect_to_db(server.app)
model.db.create_all()

fake = Faker()

# Create 10 random users with unique emails
for n in range(10):
    email = f'user{n}@test.com'
    password = f'testpassword{n}'
    full_name = fake.name()
    birthday = datetime.strptime(fake.date(), '%Y-%m-%d')
    created_at = datetime.strptime(fake.date(), '%Y-%m-%d')

    crud.create_user(email, password, full_name, birthday, created_at)
