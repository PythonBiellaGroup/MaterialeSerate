from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config

# Use bootstrap with the app
bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    # NOTE! These imports need to come after you've defined db, otherwise you will
    # get errors in your models.py files.
    ## Grab the blueprints from the other views.py files for each "app"
    from project.corsi.routes import corsi_blueprint
    app.register_blueprint(corsi_blueprint, url_prefix="/corsi")

    from project.tags.routes import tags_blueprint
    app.register_blueprint(tags_blueprint, url_prefix="/tags")
    
    from project.serate.routes import serate_blueprint
    app.register_blueprint(serate_blueprint, url_prefix="/serate")
    
    from project.error_pages.routes import error_pages_blueprint
    app.register_blueprint(error_pages_blueprint)

    from project.main.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    
    return app



