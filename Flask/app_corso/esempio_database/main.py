import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.sqlite

BASEDIR = os.path.abspath(os.path.dirname(__name__))
print(f"Base Directory: {BASEDIR}")

app = Flask(__name__)

# configurare il path del database e alcune informazioni
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    BASEDIR, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

# aggiungiamo sqlalchemy all'applicazione
db = SQLAlchemy(app)


# Definizione corsi
class Corso(db.Model):

    # nome della tabella
    __tablename__ = "corso"

    # definizione della struttura della tabella
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    insegnante = db.Column(db.Text)
    allievi = db.Column(db.Integer)

    # definire il costruttore
    def __init__(self, nome, insegnante, allievi):
        self.nome = nome
        self.insegnante = insegnante
        self.allievi = allievi

    # definiamo il print dell'oggetto
    def __repr__(self):
        message = f"\nCorso: {self.nome} insegnato da: {self.insegnante}, con numero di allievi: {self.allievi} con id: {self.id}"
        return message
