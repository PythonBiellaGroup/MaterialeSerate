import os
import logging
from logging.handlers import RotatingFileHandler

from src.common.utils import read_yaml, get_folder_path

# Set the logs
VERBOSITY = os.getenv(
    "VERBOSITY", "debug"
)  # info as default, #debug for local dev

LOG_PATH = os.getenv("LOG_PATH", "./logs")


# Define the logs
# Set verbosity
def configure_logging(verbosity=VERBOSITY, log_path=LOG_PATH):
    log_level = logging.getLevelName(verbosity.upper())
    if isinstance(log_level, int):
        logging.basicConfig(
            level=log_level,
            format="[%(levelname)s] %(asctime)s | %(message)s | in function: %(funcName)s",
            handlers=[
                RotatingFileHandler(
                    os.path.join(log_path, "info.log"),
                    maxBytes=10000,
                    backupCount=10,
                ),
                logging.StreamHandler(),
            ],
        )
        result = True
    else:
        result = False
        raise NotImplementedError(
            f"Logging level {VERBOSITY.upper()} does not exist!"
        )
    return result


# Read the application configuration settings
yaml_path = os.path.join(get_folder_path("."), "config")


# ETL Configs
ETL_CONFIG = read_yaml(yaml_path, filename="etl.yml")
ETL_DATASET_CONFIG = ETL_CONFIG["dataset"]  # name of the datasets
ETL_DATA_CONFIG = ETL_CONFIG["etl"]  # remote input
ETL_EXTRACTION_CONFIG = ETL_CONFIG["etl_results"]  # file on disk
ETL_DATA_PATH = ETL_CONFIG["data_path"]
ETL_CSV_ARGS = ETL_CONFIG["csv_args"]

# App configs
APP_CONFIG = read_yaml(yaml_path, filename="settings.yml")
APP_DATASET_CONFIG = APP_CONFIG["dataset"]
APP_CSV_ARGS = APP_CONFIG["csv_args"]
APP_DATA_PATH = os.getenv("DATA_PATH", APP_CONFIG["data_path"])