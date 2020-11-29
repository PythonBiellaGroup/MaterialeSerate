'''
Per eseguire:

set FLASK_APP=app.py
set FLASK_DEBUG=true
flask run

oppure

python app.py

Per cambiare configurazione da ambiente:
set FLASK_CONFIG=...

'''

import os
from project import create_app, db
from flask import render_template
from flask_migrate import Migrate


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# Create db and migrations
Migrate(app, db)

'''
Per "navigare" in modalità shell
Use shell_context_processor() to add other automatic imports.
'''
@app.shell_context_processor
def make_shell_context():
 return dict(db=db, Tag=Tag, Corso=Corso, Serata=Serata, Ruolo=Ruolo, Utente=Utente, Post=Post, Comment=Comment)

'''
Per i test di unità automatici, il decorator
app.cli.command permette di creare comandi "custom".
Il nome della funzione "decorata", in questo caso "test" sarà il comando per richiamarla.
In questo caso l'implementazione di test() invoca il test runner del package unittest.

Quindi per lanciare i test automatici:

set FLASK_APP=app.py
flask test

'''
@app.cli.command()
def test():
 """Run the unit tests."""
 import unittest
 # tests è il modulo
 tests = unittest.TestLoader().discover('tests')
 unittest.TextTestRunner(verbosity=2).run(tests)

'''
Prova "flask pippo" :-)
'''
@app.cli.command()
def pippo():
    print("Bravo! Hai capito come funziona il decorator cli di flask")

if __name__ == "__main__":
    app.run()