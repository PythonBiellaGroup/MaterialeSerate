import re
import unittest
from project import create_app, db
from project.serate.models import Serata
from project.corsi.models import Corso
from project.tags.models import Tag

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Tag.insert_test_tags()
        self.client = self.app.test_client()
        #self.client = self.app.test_client(use_cookies=True)
        '''
        self.client instance variable is the Flask test client object. 
        This object exposes methods that issue requests into the application
        
        When the test client is created with the use_cookies option enabled, 
        it will accept and send cookies in the same way browsers do, so functionality
        that relies on cookies to recall context between requests can be used
        '''


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_lista_serate(self):
        response = self.client.get('/serate/prossime')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Python Biella Group' in response.get_data(as_text=True))

    def test_lista_tags(self):
        response = self.client.get('/tags/')
        # Funzione visibile solo da utenti autenticati
        self.assertEqual(response.status_code, 302)

