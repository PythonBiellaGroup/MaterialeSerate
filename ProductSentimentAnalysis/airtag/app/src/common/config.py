import os

import tweepy
from dotenv import load_dotenv
from tweepy import OAuthHandler

# from app.src.common.utils import read_yaml
# from app.src.common.logger import logger


# Set the application variables
APP_NAME: str = os.environ.get("APP_NAME", "Test")
# if you want to test gunicorn the below environment variabile must be False
DEBUG_MODE: str = os.environ.get("DEBUG_MODE", "True")
VERBOSITY: str = os.environ.get("VERBOSITY", "DEBUG")

# Application Path
APP_PATH: str = os.environ.get("PROJECT_WORKSPACE", os.path.abspath("."))
CONFIG_PATH: str = os.path.join(APP_PATH, "app", "config")
STATIC_PATH: str = os.path.join(APP_PATH, "app", "static")
DATA_PATH: str = os.path.join(APP_PATH, "data")

# Read the dotenv file
DOTENV_PATH = os.path.join(APP_PATH, "vars.env")
load_dotenv(DOTENV_PATH)

# twitter API credentials
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
AUTH = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
API = tweepy.API(AUTH)

# azure cognitive services credentials
AZURE_KEY = os.getenv("CG_KEY")
AZURE_ENDPOINT = os.getenv("CG_ENDPOINT")

# Database settings
DB_CONFIG: dict = {
    "db_name": os.getenv("DB_NAME", "test"),
    "db_user": os.getenv("DB_USER", "root"),
    "db_password": os.getenv("DB_PASSWORD", "SUPERpw42"),
    "db_port": os.getenv("DB_PORT", "5492"),
    "db_host": os.getenv("DB_HOST", "localhost"),
}

# Read the configurations
# APP_CONFIG: dict = read_yaml(CONFIG_PATH, filename="settings.yml")

# logging
# logger.debug(f"App path: {APP_PATH}")
# logger.debug(f"Config path: {CONFIG_PATH}")
# logger.debug(f"Config path: {STATIC_PATH}")
# logger.debug(f"Data Path: {DATA_PATH}")
