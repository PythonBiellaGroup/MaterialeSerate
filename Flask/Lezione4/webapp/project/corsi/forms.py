from time import strftime
from flask_wtf import FlaskForm
from project.models.corsi import Corso
from project.models.serate import Serata
from project import db
from wtforms import (
    Form,
    validators,
    StringField,
    IntegerField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
)


class CorsiForm(FlaskForm):

    # def __init__(self, input_list):
    # Generate choices for selections in the form
    # super().__init__()
    # self.course_serate.choices = input_list

    course_level_list = [
        ("principiante", "principiante"),
        ("facile", "facile"),
        ("medio", "medio"),
        ("avanzato", "avanzato"),
        ("esperto", "esperto"),
    ]

    # String field: Name of the course
    course_name = StringField(
        "Name of the course",
        validators=[
            validators.Length(min=1, max=120),
            validators.required("Please insert name of the course"),
        ],
    )
    # String field: Course Teacher
    course_teacher = StringField(
        "Teacher",
        validators=[
            validators.Length(min=1, max=120),
            validators.required("Please insert name of the teacher"),
        ],
    )
    # Integer Field: Number of lessons
    course_lessons = IntegerField(
        "Number of lessons",
        validators=[validators.required("Please define a number of lessons")],
    )

    # # Multiple select field
    # # Numero di serate
    # course_serate = SelectField(
    #     "Prima serata",
    #     choices=test_list,
    #     validators=[validators.required("Seleziona la prima serata del corso")],
    # )

    # Livello di difficoltà del corso
    course_level = SelectField(
        "Livello del corso",
        choices=course_level_list,
        validators=[
            validators.required("Definisci il livello di difficoltà del corso")
        ],
    )

    # Boolean Field
    course_multiple = BooleanField("Corso con molte serate?")

    # Free Text: Descrizione del corso
    course_description = TextAreaField("Descrizione del corso")

    # Submit button
    submit = SubmitField("Create New Course")


# Utilities functions
def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time


def write_to_disk(name, surname, email):
    data = open("file.log", "a")
    timestamp = get_time()
    data.write(
        "DateStamp={}, Name={}, Surname={}, Email={} \n".format(
            timestamp, name, surname, email
        )
    )
    data.close()


def write_db(name, teacher, lessons, level, description):

    print(f"Writing new data to db: {name}")

    new_course = Corso(name, teacher, lessons, level, description)

    # try:
    db.session.add(new_course)
    db.session.commit()
    # get the id of the object
    # db.session.refresh(new_course)
    course_inserted = Corso.query.filter_by(nome=name).first()
    print(f"Course: {name} added to db, with id: {course_inserted.id}")

    return course_inserted.id

    # except Exception as message:
    #     print(f"Impossibile to write on db the new course: {name}, because: {message}")
    #     db.session.rollback()
    #     return 0
