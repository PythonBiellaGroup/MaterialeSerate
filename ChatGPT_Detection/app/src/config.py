import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict
from dotenv import dotenv_values
from loguru import logger
from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    """
    Settings class for application settings and secrets management
    Official documentation on pydantic settings management:
    - https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # Set the application variables
    APP_NAME: str = "Test"
    PROJECT_NAME: str = "Test"
    RELEASE: str = "0.0.1"

    # Application Path
    APP_PATH: str = os.path.abspath(".")
    CONFIG_PATH: str = os.path.join(APP_PATH, "app", "config")
    DATA_PATH: str = os.path.join(APP_PATH, "app", "data")

    # EXTRA VALUES not mapped in the config but that can be existing in .env or env variables in the system
    extra: Dict[str, Any] = None

    # Open AI
    OPENAI_ORGANIZATION: str = ""
    OPENAI_API_KEY: str = ""

    # Logger
    LOG_VERBOSITY: str = "DEBUG"
    LOG_ROTATION_SIZE: str = "100MB"
    LOG_RETENTION: str = "30 days"
    LOG_FILE_NAME: str = "./logs/{time:D-M-YY}.log"
    LOG_FORMAT: str = "{time:HH:mm:ss!UTC}\t|\t{file}:{module}:{line}\t|\t{message}"
    ECS_LOG_PATH: str = "./logs/elastic.log"

    def _setup_logger(self) -> bool:
        # logger.remove() to remove default logging to StdErr
        logger.add(
            self.LOG_FILE_NAME,
            rotation=self.LOG_ROTATION_SIZE,
            retention=self.LOG_RETENTION,
            colorize=True,
            format=self.LOG_FORMAT,
            level=self.LOG_VERBOSITY,
            serialize=False,
            catch=True,
            backtrace=False,
            diagnose=False,
            encoding="utf8",
        )

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        all_required_field_names = {
            field.alias for field in cls.__fields__.values() if field.alias != "extra"
        }  # to support alias

        extra: Dict[str, Any] = {}
        for field_name in list(values):
            if field_name not in all_required_field_names:
                extra[field_name] = values.pop(field_name)
        values["extra"] = extra
        return values


def env_load(env_file: str) -> Settings:
    """
    If you want to generate settings with a specific .env file.
    Be carefull: you have to insert only the env that are in the config.
    Look into official technical documentation for more information about the variables.

    Args:
        env_file (str): The path to the .env file. (with the name)

    Returns:
        Settings: The settings object with the .env file loaded.
    """
    try:
        # get the dotenv file values into an OrderedDict
        env_settings = dotenv_values(env_file)
        # convert to normal dict
        env_settings = dict(env_settings)
        # define and create the new object
        settings = Settings(**env_settings)

        return settings
    except Exception as message:
        print(f"Error: impossible to read the env: {message}")
        return None


# cache system to read the settings without everytime read the .env file
@lru_cache()
def get_settings(settings: Settings = None, env_file: str = None, **kwargs) -> Settings:
    """
    Function to get the settings object inside the config.
    This function use lru_cache to cache the settings object and avoid to read everytime the .env file from disk (much more faster)

    Args:
        settings (Settings, optional): The settings object to use. Defaults to None.
    Returns:
        Settings: The settings object.
    """
    # define the new settings
    try:
        if not settings:
            if env_file:
                # check if env file existing
                if not Path(env_file).exists():  # nocov
                    settings = None
                    raise ValueError(f"Config file {env_file} does not exist.")
                else:
                    settings = env_load(env_file)
            else:
                settings = Settings(**kwargs)
        return settings
    except Exception as message:
        print(f"Error: impossible to get the settings: {message}")
        return None


# # define the settings (use the env file if it's used)
env_file = os.environ.get("ENV_FILE", ".env")
settings = get_settings(env_file=env_file)
settings._setup_logger()
