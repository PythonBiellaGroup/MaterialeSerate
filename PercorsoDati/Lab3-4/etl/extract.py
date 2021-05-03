# First phase of ETL: Extraction of the information in files
import os
import logging
import requests
import gzip
import shutil

import pandas as pd

from src.common.utils import check_df, get_folder_path
from config import (
    ETL_CSV_ARGS,
    ETL_DATA_PATH,
    ETL_EXTRACTION_CONFIG,
    ETL_DATA_CONFIG,
)


# Remote connector
def download_data(
    net_path: str, write_path: str, output_name: str, remove_temp=True
) -> bool:

    logging.info(f"Downloading {output_name} data from: {net_path}")
    url = net_path
    r = requests.get(url, allow_redirects=True)

    # now support only gz file
    if url.split(".")[-1] in ["gz"]:
        output_name_complete = output_name + ".gz"
        convert = True
    else:
        output_name_complete = output_name
        convert = False

    write_path_complete = os.path.join(write_path, output_name_complete)
    open(write_path_complete, "wb").write(r.content)

    if convert:
        logging.info("Unzipping the file")

        with gzip.open(write_path_complete, "rb") as f_in:
            write_path_csv = os.path.join(write_path, output_name + ".csv")
            with open(write_path_csv, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        if remove_temp:
            # Remove temporary gz and keep only the csv
            os.remove(write_path_complete)

        write_path_complete = write_path_csv

    return write_path_complete


# Read dataset simple
def read_dataset(complete_path: str, csv_arguments={}) -> pd.DataFrame:

    if csv_arguments:
        dataframe = pd.read_csv(complete_path, **csv_arguments)
    else:
        dataframe = pd.read_csv(complete_path)

    return dataframe


# Import data extract main function
def import_data(remote=False, config=ETL_DATA_CONFIG) -> dict:
    logging.info("Start importing the data")

    # Get the dataframe names
    dataframe_names = list(config.keys())
    # Get the filenames from config
    data_files = list(config.values())

    # Define all the settings for the csv reading
    pandas_csv_arguments = ETL_CSV_ARGS

    folder_path = get_folder_path(".")
    data_dir = ETL_DATA_PATH
    data_path = os.path.join(folder_path, data_dir)
    # Define the folder data path

    # Save the files names
    file1_name = data_files[0]
    file2_name = data_files[1]
    file3_name = data_files[2]

    if remote:
        # The data coming from the web, so it's important to download
        file1_name = download_data(file1_name, data_path, dataframe_names[0])
        file2_name = download_data(file2_name, data_path, dataframe_names[1])
        file3_name = download_data(file3_name, data_path, dataframe_names[2])

    listings = read_dataset(
        os.path.join(data_path, file1_name), pandas_csv_arguments
    )
    reviews = read_dataset(
        os.path.join(data_path, file2_name), pandas_csv_arguments
    )
    calendar = read_dataset(
        os.path.join(data_path, file3_name), pandas_csv_arguments
    )

    check_df(listings)
    check_df(reviews)
    check_df(calendar)

    datasets = {
        dataframe_names[0]: listings,
        dataframe_names[1]: reviews,
        dataframe_names[2]: calendar,
    }

    return datasets
