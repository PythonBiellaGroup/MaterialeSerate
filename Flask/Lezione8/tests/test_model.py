import re
import unittest
from project import create_app, db
from project.serate.models import Serata
from project.corsi.models import Corso, StatoCorso
from project.tags.models import Tag
from project.utenti.models import Utente
from project.ruoli.models import Ruolo

class FlaskModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Tag.insert_test_tags()
        Corso.insert_test_corsi()
        Serata.insert_test_serate()
        Ruolo.insert_roles()
        Utente.insert_test_users()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_check_tag(self):
        t = Tag.query.filter_by(name="Python").first()
        #print(t)
        self.assertTrue(t.name == "Python")

    def test_check_corso(self):
        c = Corso.query.filter_by(nome="Flask").first()
        #print(c)
        self.assertTrue(c.nome == "Flask")
        self.assertTrue(c.insegnante == "Andrea Guzzo e Mario Nardi")
        self.assertFalse(c.insegnante == "Mario Nardi")

    def test_check_serata(self):
        s = Serata.query.filter_by(nome="Flask 1").first()
        self.assertTrue(s.nome == "Flask 1")

    def test_check_utente(self):
        u = Utente.query.filter_by(email="test1@test.it").first()
        self.assertTrue(u.username == "maurici")
        self.assertTrue(u.password_hash is not None)
        self.assertTrue(u.verify_password('pwd1'))
        