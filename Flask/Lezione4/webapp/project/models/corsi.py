from project.models.serate import Serata
from project import db


# Tabella di relazione N:N tra Corso e Tag
tags = db.Table(
    "corso_tags",
    db.Column("corso_id", db.Integer, db.ForeignKey("corso.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Corso(db.Model):
    # Nome della tabella
    __tablename__ = "corso"

    # Struttura/Attributi
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    insegnante = db.Column(db.String(100))
    lezioni = db.Column(db.Integer())
    livello = db.Column(db.String(100))
    descrizione = db.Column(db.String(255))

    # Relazione 1:n; ordinamento serate per data
    serate = db.relationship(
        "Serata", order_by="asc(Serata.data)", backref="corso", lazy="subquery"
    )

    # Relazione n:n
    tags = db.relationship(
        "Tag", secondary=tags, lazy="subquery", backref=db.backref("corso", lazy=True),
    )

    # Costruttore

    # NOTA: Lasciare il costruttore crea problemi nella gestione della form di creazione
    def __init__(self, nome, insegnante, lezioni, livello, descrizione):
        self.nome = nome
        self.insegnante = insegnante
        self.lezioni = lezioni
        self.livello = livello
        self.descrizione = descrizione
        # self.serate = serate
        # self.tags = tags

    # Visualize object corso informations
    def __repr__(self):
        return "\n{}: {} è tenuto da {}. Livello {}. Id {}. Tags {}".format(
            self.nome,
            self.descrizione,
            self.insegnante,
            self.livello,
            self.id,
            self.tags,
        )


class Tag(db.Model):

    __tablename__ = "tag"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tag '{}'>".format(self.name)
