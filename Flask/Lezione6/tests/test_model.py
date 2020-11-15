import re
import unittest
from project import create_app, db
from project.serate.models import Serata
from project.corsi.models import Corso
from project.tags.models import Tag

class FlaskModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Tag.insert_test_tags()
        Corso.insert_test_corsi()
        Serata.insert_test_serate()
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

    def test_check_serata(self):
        s = Serata.query.filter_by(nome="Flask 1").first()
        self.assertTrue(s.nome == "Flask 1")

        