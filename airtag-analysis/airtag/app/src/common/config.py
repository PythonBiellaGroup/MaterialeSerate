import os

from app.src.common.utils import read_yaml
from app.src.logger import logger


# Set the application variables
APP_NAME: str = os.environ.get("APP_NAME", "Test")
# if you want to test gunicorn the below environment variabile must be False
DEBUG_MODE: str = os.environ.get("DEBUG_MODE", "True")
VERBOSITY: str = os.environ.get("VERBOSITY", "DEBUG")

# Application Path
APP_PATH: str = os.environ.get("PROJECT_WORKSPACE", os.path.abspath("."))
CONFIG_PATH: str = os.path.join(APP_PATH, "app", "config")
DATA_PATH: str = os.path.join(APP_PATH, "app", "data")


# Database settings
DB_CONFIG: dict = {
    "db_name": os.getenv("DB_NAME", "test"),
    "db_user": os.getenv("DB_USER", "root"),
    "db_password": os.getenv("DB_PASSWORD", "SUPERpw42"),
    "db_port": os.getenv("DB_PORT", "5492"),
    "db_host": os.getenv("DB_HOST", "localhost"),
}

# Read the configurations
APP_CONFIG: dict = read_yaml(CONFIG_PATH, filename="settings.yml")

# logging
logger.debug(f"App path: {APP_PATH}")
logger.debug(f"Config path: {CONFIG_PATH}")
logger.debug(f"Data Path: {DATA_PATH}")
