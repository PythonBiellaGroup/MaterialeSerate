## Script to import data into DB with CRUD Operations
from project.serate.models import Serata
from project.corsi.models import Corso
from project.tags.models import Tag
from project.ruoli.models import Ruolo
from project.utenti.models import Utente

from project import db,create_app
import datetime
import os

CREATE_ALL = True

if CREATE_ALL:
    # Utilizzo dell'application factory
    app = create_app('development')
    app_context = app.app_context()
    app_context.push()
    
    print("Start creating structure")    
    db.create_all()
    print("Start creating roles")
    Ruolo.insert_roles()
    
    print("Start creating users")
    Utente.insert_test_users()

    print("Start creating tags")
    Tag.insert_test_tags()

    print("Start creating corsi")
    Corso.insert_test_corsi()
    
    print("Start creating serate")
    Serata.insert_test_serate()

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