from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config
# Per modulo autenticazione Utente
from flask_login import LoginManager
# Per email
from flask_mail import Mail

# Use bootstrap with the app
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()

# Per modulo autenticazione Utente
login_manager = LoginManager()
login_manager.login_view = 'utenti.login'
# Personalizzazione del messaggio di errore su pagina che richiede autenticazione
login_manager.login_message = u"Autenticati per vedere questa pagina"
login_manager.login_message_category = "info"

def create_app(config_name):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    # Per modulo autenticazione Utente
    login_manager.init_app(app)

    # NOTE! These imports need to come after you've defined db, otherwise you will
    # get errors in your models.py files.
    ## Grab the blueprints from the other routes.py files for each "app"
    from project.utenti.routes import utenti_blueprint
    app.register_blueprint(utenti_blueprint, url_prefix="/utenti", url_static="../static")

    from project.corsi.routes import corsi_blueprint
    app.register_blueprint(corsi_blueprint, url_prefix="/corsi", url_static="../static")

    from project.tags.routes import tags_blueprint
    app.register_blueprint(tags_blueprint, url_prefix="/tags", url_static="../static")
    
    from project.serate.routes import serate_blueprint
    app.register_blueprint(serate_blueprint, url_prefix="/serate", url_static="../static")
    
    from project.error_pages.routes import error_pages_blueprint
    app.register_blueprint(error_pages_blueprint)

    from project.main.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app



