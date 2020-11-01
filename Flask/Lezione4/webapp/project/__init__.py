import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from project.utilities.utility import get_folder_path, define_path, read_yaml_file

app = Flask(__name__, static_folder="static")

# Use bootstrap with the app
Bootstrap(app)

# Base directory with yaml configurations to app
basedir = os.path.abspath(os.path.dirname(__file__))
basedir_path = Path(basedir)  # basedir with pathlib (much more usefull)
yml_configurations = read_yaml_file(basedir_path.parent, "keys.yml")

# Define configs for the app
app.config["SECRET_KEY"] = yml_configurations["secret_key"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create db and migrations
db = SQLAlchemy(app)
Migrate(app, db)


# NOTE! These imports need to come after you've defined db, otherwise you will
# get errors in your models.py files.
## Grab the blueprints from the other views.py files for each "app"
from project.corsi.views import corsi_blueprint
from project.error_pages.handlers import error_pages

app.register_blueprint(corsi_blueprint, url_prefix="/corsi")
app.register_blueprint(error_pages)

# app.register_blueprint(serate_blueprint, url_prefix="/serate")

