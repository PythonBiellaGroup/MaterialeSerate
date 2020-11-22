'''
Note per la configurazione in PRODUZIONE
Valorizzare:
FLASK_APP=app.py
FLASK_CONFIG=production
SECRET_KEY=...tbd...
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_USE_TLS=true
PBG_ADMIN=
'''
import os
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "supersupersupersecretkey"
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # Costanti usati nelle mail registrazione utenti
    PBG_MAIL_SUBJECT_PREFIX = '[Python Biella Group]'
    PBG_MAIL_SENDER = 'Python Biella Group Admin <pbg@pbg.com>'
    # Definizione email dell'utente ADMIN iniziale
    PBG_ADMIN = os.environ.get('PBG_ADMIN')

    @staticmethod
    def init_app(app):
        pass    

class ProdConfig(Config):    
    pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    DEBUG = True
    # Settings per usare https://mailtrap.io/ - Registrati e cambia con i tuoi dati
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_USERNAME = '9a973adb59007f'
    MAIL_PASSWORD = '4f5fd306232d45'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    PBG_ADMIN = "burlesco70@test.it"


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "testdata.sqlite")
    # To test configuration usage in unit test
    TESTING = True 
    # disabling CSRF protection in the testing conguration
    WTF_CSRF_ENABLED = False
    # test admin
    PBG_ADMIN = "test1@test.it"

config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}
