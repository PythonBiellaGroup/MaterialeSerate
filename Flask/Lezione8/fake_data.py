## Script to import data into DB with CRUD Operations
from project.serate.models import Serata
from project.corsi.models import Corso
from project.tags.models import Tag
from project.ruoli.models import Ruolo
from project.utenti.models import Utente
from project.blog.models import Post
from project.commenti.models import Comment

from project import db,create_app
import datetime
import os
from random import randint
from  faker import Faker

def users(count=100):
    fake = Faker('it_IT')
    i = 0
    while i < count:
        u = Utente(email=fake.email(),
            username=fake.user_name(),
            password='password',
            confirmed=True,
            name=fake.name(),
            location=fake.city(),
            about_me=fake.text(),
            member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def posts(count=100):
    fake = Faker('it_IT')
    user_count = Utente.query.count()
    for i in range(count):
        u = Utente.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                timestamp=fake.past_date(),
                author=u)
        db.session.add(p)
        db.session.commit()

def comments(count=100):
    fake = Faker('it_IT')
    user_count = Utente.query.count()
    post_count = Post.query.count()
    for i in range(count):
        u = Utente.query.offset(randint(0, user_count - 1)).first()
        p = Post.query.offset(randint(0, post_count - 1)).first()
        c = Comment(body=fake.text(),
                 timestamp=fake.past_date(),
                 post=p,
                 author=u)
        db.session.add(c)
        db.session.commit()          
            
CREATE_ALL = True

if CREATE_ALL:
    # Utilizzo dell'application factory
    app = create_app('development')
    app_context = app.app_context()
    app_context.push()
    
    print("Creating structure")    
    db.create_all()

    print("Creating roles")
    Ruolo.insert_roles()
    
    print("Creating fake users")
    users(10)
    print("Creating test users")
    Utente.insert_test_users()

    print("Creating tags")
    Tag.insert_test_tags()

    print("Creating corsi")
    Corso.insert_test_corsi()
    
    print("Creating serate")
    Serata.insert_test_serate()

    print("Creating posts fake")
    posts()

    print("Creating commenti fake")    
    comments()

###DEBUGS
print("\n#### DATA DEBUG ####\n")

# Read a course
courses = Corso.query.all()
print(f"\nList of all courses: {courses}")

# Get a course by name
c = Corso.query.filter_by(nome="Flask").first()  # Ritorna il corso di Flask
print(f"\nFlask course: {c}")

# Get all serate
list_serate = Serata.query.all()
print(f"\nSerate create:")
for serata in list_serate:
    print(f"Serata: {serata.id}, {serata.nome}, in data: {serata.data}")

# Get a serate by serate name
list_impostare = Serata.query.filter(Serata.nome.like("%impostare%")).all()
print(f"\nSerate da impostare:")
for i in list_impostare:
    print(f"Serate ancora da impostare: {i.id}, {i.nome}, in data: {i.data}")

db.session.remove()