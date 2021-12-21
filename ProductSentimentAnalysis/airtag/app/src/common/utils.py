import os
import yaml
import re
import json
import datetime as dt
import importlib

import unidecode
import numpy as np
import pandas as pd

from app.src.logger import logger


# Conversions
def underscore_to_camelcase(text):
    return "".join(x.capitalize() for x in text.split("_"))


def millis2date(ms):
    return dt.datetime.fromtimestamp(ms / 1000.0) if pd.notnull(ms) else None


def date2millis(x, format="%Y-%m-%d %H:%M:%S"):
    return dt.datetime.strptime(x, format).timestamp() * 1000 if pd.notnull(x) else None


def parse_date(x, format="%Y-%m-%d %H:%M:%S"):
    return dt.datetime.strptime(x, format).date()


def date_to_string(x, format="%Y-%m-%d %H:%M:%S"):
    return x.strftime(format) if not pd.isnull(x) else np.nan


def string_to_date(x, format="%Y-%m-%d %H:%M:%S"):
    if isinstance(x, str):
        return dt.datetime.strptime(x, format).date() if not pd.isnull(x) else np.nan
    elif isinstance(x, dt.date):
        return x
    else:
        return np.nan


def parsedates(column):
    """Convert Series from string to date

    Args:
        column (pd.Series): date string column

    Returns:
        [pd.Series]: datetime column
    """
    column_stripped = column.astype(str).str.strip()
    return pd.to_datetime(column_stripped, format="%d-%b-%y")


def parsedates_withhour(column):
    """Convert Series from string to date

    Args:
        column (pd.Series): date string column

    Returns:
        [pd.Series]: datetime column
    """
    column_stripped = column.astype(str).str.strip()
    try:
        return pd.to_datetime(column_stripped, format="%d/%m/%Y %H:%M:%S")
    except Exception as message:
        logger.warning(f"date {column.name} has wrong format! {message}")
        return pd.to_datetime(
            column_stripped, format="%d/%m/%Y %H:%M:%S", errors="coerce"
        )


def string_contains(x, words):
    return any([w in x for w in words])


def cutstring(column, stop=3):
    return column.astype(str).str.slice(stop=stop)


def as_list(x):
    if isinstance(x, list):
        return x
    else:
        return [x]


def logging_list(log_list, l_name="", level="DEBUG"):
    logger.log(getattr(logger, level), l_name)
    for i in sorted(log_list):
        logger.log(getattr(logger, level), i)
    logger.log(getattr(logger, level), "")


def remove_columns(dataset, cols):
    if isinstance(cols, str):
        cols = [cols]
    cols = [c for c in cols if c in dataset.columns]
    dataset = dataset.drop(cols, axis=1)
    return dataset


def keep_columns(df, cols):
    if isinstance(cols, str):
        cols = [cols]
    cols = [c for c in cols if c in df.columns]
    df = df.loc[:, cols]
    return df


def keep_only_columns(dataset, cols):
    if isinstance(cols, str):
        cols = [cols]
    cols = [c for c in dataset.columns if c not in cols]
    dataset = dataset.drop(cols, axis=1)
    return dataset


def save_dict_to_json(d, file):
    with open(file, "w") as fp:
        json.dump(d, fp, sort_keys=True, indent=4)


def load_class(path_to_module, class_name):
    module = importlib.import_module(path_to_module)
    return getattr(module, class_name)


# Check Dataframe Utility function
def check_df(dataframe, sample=False):

    logger.info(
        f"Dataframe Shape: {dataframe.shape} with rows: {dataframe.shape[0]} and columns: {dataframe.shape[1]}"
    )
    logger.info(f"\nDF Columns: \n{list(dataframe.columns)}")
    if sample:
        logger.info(f"\nData:\n{dataframe.head(5)}")

    return None


# FILES
def check_if_file_exists(file):
    if os.path.exists(file) and os.path.isfile(file):
        return True
    else:
        return False


def read_file(file):
    file_ext = os.path.splitext(file)[1]
    if file_ext == ".csv":
        return pd.read_csv(file)
    elif file_ext == ".xlsx":
        return pd.read_excel(file, sheet_name=0)
    else:
        raise NotImplementedError(
            "Reading of files with extension " + file_ext + " is not implemented."
        )


def write_file(df, file):
    file_ext = os.path.splitext(file)[1]
    if file_ext == ".csv":
        df.to_csv(file, index=False)
    elif file_ext == ".xlsx":
        df.to_excel(file, index=False)
    else:
        raise NotImplementedError(
            "Saving of files with extension " + file_ext + " is not implemented."
        )


def remove_special_characters(s):
    return (
        unidecode.unidecode(s)
        .replace("/", "_")
        .replace("-", "_")
        .replace("(", "_")
        .replace(")", "_")
        .replace(".", "_")
        .replace(" ", "_")
        .replace("&", "and")
        .replace("'", "")
        .replace("__", "_")
        .replace("___", "_")
        .lower()
    )


# Yaml Library and functions
def get_folder_path(custom_path: str = "", force_creation: bool = False) -> str:
    """Get the folder absolute path starting from a relative path of your python launch file.
    This function is os independent, so it's possibile to use everywherre

    Args:
        custom_path (str, optional): The relative path of your path search. Defaults to "".
        force_creation (bool, optional): if the path doesn't exist, force the creation of the folder. Defaults to False.

    Returns:
        str: The absolute path you want to search
    """

    if custom_path == "" or custom_path is None:
        BASEPATH = os.path.abspath("")
    else:
        BASEPATH = os.path.abspath(custom_path)

    # Check if the folder exist, if not exit you can create with a flag
    if not os.path.exists(BASEPATH):
        logger.error("WARNING: Path doesn't exist")
        if force_creation:
            logger.debug("Force creation folder")
            try:
                os.makedirs(BASEPATH)
            except Exception as message:
                logger.error(f"Impossible to create the folder: {message}")

    logger.debug(f"PATH: {BASEPATH}, force creation: {force_creation}")
    return BASEPATH


def checkpath(to_path: str, filename: str) -> str:
    """
    Check path and filename
    Search a specific filename into a folder path

    Args:
        to_path (str): path where you want to search
        filename (str): filename

    Returns:
        str: the path where the file is
    """
    try:
        if to_path == "" or to_path is None:
            to_path = get_folder_path("./")

        if filename == "" or filename is None:
            filename = "result.yml"

        if re.search(r"yml", filename) is False:
            filename = filename + ".yml"

        file_path = os.path.join(to_path, filename)
        return file_path

    except Exception as message:
        logger.error(f"Path: {to_path}, or filename: {filename} not found: {message}")
        return None


def read_yaml(file_path: str, filename: str = "") -> dict:
    """Read a yaml file from disk

    Args:
        file_path (str): path where you want to load
        filename (str, optional): Name of the file you want to load. Defaults to "".

    Returns:
        dict: The dictionary readed from the yaml file
    """
    file_path = checkpath(file_path, filename)

    try:
        with open(file_path) as file:

            data = yaml.safe_load(file)
            file.close()
        logger.debug(f"Yaml file: {filename} loaded")
        return data

    except Exception as message:
        logger.error(f"Impossible to load the file: {filename} with path: {file_path}")
        logger.error(f"Error: {message}")
        return None


def write_dataset_yaml(
    to_path: str = "", filename: str = "", dataset: pd.DataFrame = None
) -> bool:
    """Write a pandas dataset to yaml

    Args:
        to_path (str, optional): Path where you want to save the yaml file. Defaults to "".
        filename (str, optional): Name of the file to use. Defaults to "".
        dataset (pd.DataFrame, optional): Pandas dataframe to save. Defaults to None.

    Returns:
        bool: If the
    """
    file_path = checkpath(to_path, filename)

    if not isinstance(dataset, pd.DataFrame):
        logger.error("Please use a Pandas dataframe with write_dataset_yaml function")
        return False

    try:
        with open(file_path, "w") as file:
            yaml.dump(dataset, file)
        file.close()
        logger.debug(f"File successfully write to: {file_path}")
        return True

    except Exception as message:
        logger.error(f"Impossible to write the file: {message}")
        return False


def write_yaml(to_path, filename, obj_save):
    """
    Write some properties to generic yaml file
    :param to_path: where you want to save your file
    :param filename: name of the file
    :param obj_save: the object you want to save
    :return: a boolean with success or insuccess
    """
    file_path = checkpath(to_path, filename)

    try:
        with open(file_path, "w") as file:
            yaml.dump(obj_save, file)
        file.close()
        logger.debug(f"File successfully write to: {file_path}")
        return True

    except Exception as message:
        logger.error(f"Impossible to write the file: {message}")
        return False
