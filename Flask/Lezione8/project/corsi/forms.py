from time import strftime
from flask_wtf import FlaskForm
from wtforms import (
    Form,
    validators,
    StringField,
    IntegerField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
    DateField
)
from wtforms.validators import DataRequired, Length

'''
Corso Form
'''
class CorsiForm(FlaskForm):

    course_level_list = [
        ("principiante", "Principiante"),
        ("facile", "Facile"),
        ("medio", "Medio"),
        ("avanzato", "Avanzato"),
        ("esperto", "Esperto"),
    ]

    # String field: Name of the course
    name = StringField(
        "Name of the course",
        validators=[
            validators.Length(min=1, max=120),
            validators.required("Inserisci il nome del corso"),
        ],
    )
    # String field: Course Teacher
    teacher = StringField(
        "Teacher",
        validators=[
            validators.Length(min=1, max=120),
            validators.required("Inserisci il nome dell'insegnante"),
        ],
    )

    # Livello di difficoltà del corso
    level = SelectField(
        "Livello del corso",
        choices=course_level_list,
        validators=[
            validators.required("Definisci il livello di difficoltà del corso")
        ],
    )

    # Free Text: Descrizione del corso
    description = TextAreaField("Descrizione del corso")

    # Submit button
    submit = SubmitField("Crea nuovo corso")


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