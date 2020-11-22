from project import db
from project.tags.models import Tag

'''
Oggetti Tabella relativi al modulo "corsi"
'''
# corso_tags - tabella di relazione N:N tra Corso e Tag
tags = db.Table(
    "corso_tags",
    #__table_args__ = {'extend_existing': True},
    db.Column("corso_id", db.Integer, db.ForeignKey("corso.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

# corso - tabella con i corsi
class Corso(db.Model):
    # Nome della tabella
    __tablename__ = "corso"

    # Struttura/Attributi
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    insegnante = db.Column(db.String(100))
    livello = db.Column(db.String(100))
    descrizione = db.Column(db.String(255))
    # Immagine logo da cartella static, se presente
    logo_img = db.Column(db.String(100))

    # Relazione 1:n; ordinamento serate per data
    serate = db.relationship(
        "Serata", order_by="asc(Serata.data)", backref="corso", lazy="subquery"
    )

    # Relazione n:n
    tags = db.relationship(
        "Tag", secondary=tags, lazy="subquery", backref=db.backref("corso", lazy=True),
    )

    # Costruttore
    def __init__(self, nome, insegnante, livello, descrizione, logo_img=""):
        self.nome = nome
        self.insegnante = insegnante
        self.livello = livello
        self.descrizione = descrizione
        self.logo_img = logo_img
        # self.serate = serate
        # self.tags = tags

    # Visualize object corso informations
    def __repr__(self):
        return "\n{}: {} è tenuto da {}. Livello {}. Id {}. Tags {}. Logo {}".format(
            self.nome,
            self.descrizione,
            self.insegnante,
            self.livello,
            self.id,
            self.tags,
            self.logo_img,
        )

    '''
    Utile per i test (sempre)
    e come dati iniziali prima della messa in effettivo del progetto
    '''
    @staticmethod
    def insert_test_corsi():

        corsi = [ 
            ( "Flask", "Andrea Guzzo", "Intermedio", "Corso in cinque serate del microframework Flask", "flask-icon.png" ),
            ( "Pygame", "Mario Nardi", "Principiante", "Introduzione a Pygame", "pygame-icon.png" ),
            ( "Pandas", "Maria Teresa Panunzio", "Intermedio", "Corso base per manipolare i dataframes" )
        ]
        
        # Prende i tags dal db
        python_tag = Tag.query.filter_by(name="Python").first()
        flask_tag = Tag.query.filter_by(name="Flask").first()
        wd_tag = Tag.query.filter_by(name="Web Development").first()
        sa_tag = Tag.query.filter_by(name="SqlAlchemy").first()
        pg_tag = Tag.query.filter_by(name="Pygame").first()
        g_tag = Tag.query.filter_by(name="Graphics").first()
        pandas_tag = Tag.query.filter_by(name="Pandas").first()
        numpy_tag = Tag.query.filter_by(name="NumPy").first()
        
        # Associa i tag al nome corso
        tag_dict = {}
        tag_dict["Flask"] = [ python_tag, flask_tag, wd_tag, sa_tag ]
        tag_dict["Pygame"] = [ python_tag, pg_tag, g_tag ]
        tag_dict["Pandas"] = [ python_tag, pandas_tag, numpy_tag ]

        for cor in corsi:
            # Check se già presente
            corso = Corso.query.filter_by(nome=cor[0]).first()
            if corso is None:
                # *tupla permette di usare la tupla come lista di parametri del costruttore
                # The * operator simply unpacks the tuple and passes them as the positional arguments to the function
                corso = Corso(*cor)
                # Aggiunta tag
                corso.tags = tag_dict[corso.nome]
            db.session.add(corso)
        db.session.commit()