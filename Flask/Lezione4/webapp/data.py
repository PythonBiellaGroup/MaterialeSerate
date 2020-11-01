##Script to import data into DB with CRUD Operations
from project.models.corsi import Corso, Tag
from project.models.serate import Serata
from project import db
import datetime
import os

CREATE_ALL = False


if CREATE_ALL:
    # Create entities
    db.create_all()
    print("Start creating structure")

    #################################################
    ####### 1. Create tags #######
    print("Start creating tags")

    t1 = Tag("Python")
    t2 = Tag("Flask")
    t3 = Tag("Pygame")
    t4 = Tag("SqlAlchemy")
    t5 = Tag("Web Development")
    t6 = Tag("Graphics")

    tags = [t1, t2, t3, t4, t5, t6]

    for t in tags:
        try:
            db.session.add(t)
            db.session.commit()
        except Exception as e:
            print(f"Eccezione: {e}")
            db.session.rollback()

    #################################################
    ##### 2. Create courses ######
    # Relazione n:n TAG - CORSO
    print("Start creating corsi")

    corsoFlask = Corso(
        "Flask",
        "Andrea Guzzo",
        5,
        "Intermedio",
        "Corso in cinque serate del microframework Flask",
    )
    corsoFlask.tags = [t1, t2, t4, t5]

    # Relazione n:n TAG - CORSO
    corsoPygame = Corso(
        "Pygame", "Mario Nardi", 3, "Principiante", "Introduzione a Pygame"
    )
    corsoPygame.tags = [t1, t3, t6]

    corso_pandas = Corso(
        "Pandas",
        "Maria Teresa",
        2,
        "Intermedio",
        "Corso base per manipolare i dataframes",
    )

    corsi = [corsoFlask, corsoPygame, corso_pandas]

    for c in corsi:
        try:
            db.session.add(c)
            db.session.commit()
        except Exception as e:
            print(f"Eccezione: {e}")
            db.session.rollback()

    #################################################
    ##### 3. Create Serate ######
    print("Start creating serate")

    c = Corso.query.filter_by(nome="Flask").first()  # Ritorna tutti i risultati
    s1 = Serata(
        "Da impostare",
        "1 - Introduzione a Flask e ai web server con Jinja Base",
        datetime.date(2020, 10, 12),
    )
    s2 = Serata(
        "Flask serata 2", "2 - Jinja avanzato e Forms", datetime.date(2020, 10, 19)
    )
    s3 = Serata("Flask serata 3", "3 - Flask con Database", datetime.date(2020, 10, 26))
    s4 = Serata(
        "Flask serata 4", "4 - Large Flask Applications", datetime.date(2020, 11, 2)
    )
    s5 = Serata(
        "Flask serata 5",
        "5 - REST Backend e concetti avanzati",
        datetime.date(2020, 11, 9),
    )

    si6 = Serata("Da impostare", "Non ancora definita", datetime.date(2020, 11, 10))
    si7 = Serata("Da impostare", "Non ancora definita", datetime.date(2020, 11, 11))
    si8 = Serata("Da impostare", "Non ancora definita", datetime.date(2020, 11, 12))
    s1.corso_id = c.id
    s2.corso_id = c.id
    s3.corso_id = c.id
    s4.corso_id = c.id
    s5.corso_id = c.id

    serate = [s1, s2, s3, s4, s5, si6, si7, si8]
    for s in serate:
        try:
            db.session.add(s)
            db.session.commit()
        except Exception as e:
            print(f"Eccezione: {e}")
            db.session.rollback()


#################################################
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

