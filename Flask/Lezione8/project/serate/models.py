from project import db
import datetime

from project.corsi.models import Corso

# Tabella di relazione 1 Corso : N Serate
class Serata(db.Model):

    __tablename__ = "serata"

    __table_args__ = (db.UniqueConstraint("id", "data", name="constraint_serata"),)

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descrizione = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime(), nullable=False)
    link_partecipazione = db.Column(db.String(255), nullable=True)
    link_registrazione = db.Column(db.String(255), nullable=True)

    corso_id = db.Column(db.Integer(), db.ForeignKey("corso.id"))

    def __init__(self, nome, descrizione, data, link_partecipazione='', link_registrazione=''):        
        self.nome = nome
        self.descrizione = descrizione
        self.data = data
        self.link_partecipazione = link_partecipazione
        self.link_registrazione = link_registrazione

    def __repr__(self):
        return "<Descrizione '{}'. Link registrazione>".format(self.descrizione, self.link_registrazione)

    @staticmethod
    def insert_test_serate():
        lista_serate = [
            ("Flask 1", "Introduzione a Flask e ai web server con Jinja Base", datetime.datetime(2020, 10, 12, hour=20), '', 'https://www.youtube.com/watch?v=FPI5-oGKiVI&t=759s'),
            ("Flask 2", "Jinja avanzato e Forms", datetime.datetime(2020, 10, 19, hour=20), '', 'https://www.youtube.com/watch?v=C-iEkd-BpE4'),
            ("Flask 3", "Flask con Database", datetime.datetime(2020, 10, 26, hour=20), '', 'https://www.youtube.com/watch?v=rCXhuSiOcZU'),
            ("Flask 4", "Review con Andrea", datetime.datetime(2020, 11, 2, hour=20), '', 'https://www.youtube.com/watch?v=izIKXOrbI5U'),
            ("Flask 5", "Review con Mario", datetime.datetime(2020, 11, 9, hour=20), '', 'https://vimeo.com/478050019'),
            ("Flask 6", "Blueprints, refactoring e tests con Mario", datetime.datetime(2020, 11, 16, hour=20), 'https://zoom.us/j/99953652561?pwd=NFpGVzBJazJXOW5MMEQvNFBrVnNLUT09', 'https://vimeo.com/480155611'),
            ("Flask 7", "Autenticazione con Mario", datetime.datetime(2020, 11, 23, hour=20), 'https://zoom.us/j/95155339456?pwd=Zk1wcVViazMvdkt0SlhJZENyZ0Iydz09', ''),
            ("Flask 8", "Profili, ruoli e blog con Mario", datetime.datetime(2020, 11, 30, hour=20), '', ''),            
        ]
        corso_flask = Corso.query.filter_by(nome="Flask").first()
        for serata in lista_serate:
            serata_db = Serata.query.filter_by(nome=serata[0]).first()
            if serata_db is None:
                serata_db = Serata(*serata)
                serata_db.corso_id = corso_flask.id
                db.session.add(serata_db)
            db.session.commit()
        

'''

    s1.corso_id = c.id
    s2.corso_id = c.id
    s3.corso_id = c.id
    s4.corso_id = c.id
    s5.corso_id = c.id
    s6.corso_id = c.id
    s7.corso_id = c.id

    data_serata = data_serata.replace(day=30)
    si6 = Serata("Da impostare", "Non ancora definita", data_serata)

    serate = [s1, s2, s3, s4, s5, s6, s7, si6]
'''