import unittest
from flask import current_app
from project import create_app, db


class BasicsTestCase(unittest.TestCase):
    # Eseguito prima di ogni test
    def setUp(self):
        # Crea l'app con configurazione 'testing'
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    # Eseguito dopo ogni test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        # Controlla la configurazione tramite check su settaggio ad hoc
        self.assertTrue(current_app.config['TESTING'])