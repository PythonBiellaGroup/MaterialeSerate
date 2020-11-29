from project import db
from sqlalchemy import desc,asc

class Tag(db.Model):

    __tablename__ = "tag"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tag '{}'>".format(self.name)
    
    '''
    Utile per il popolamento dei dati e per i test
    '''
    @staticmethod
    def insert_test_tags():
        tags = [ 
            "Python", "Flask", "Pygame",
            "SqlAlchemy", "Web Development", "Graphics",
            "NumPy", "Pandas", "Django"
        ]
        for name_tag in tags:
            tag = Tag.query.filter_by(name=name_tag).first()
            if tag is None:
                tag = Tag(name=name_tag)
            db.session.add(tag)
        db.session.commit()

    @staticmethod
    def all_tags_selection():
        lista_tags = Tag.query.order_by(asc(Tag.name)).all()
        selection = []
        for t in lista_tags:
            selection.append((t,t))
        return selection
