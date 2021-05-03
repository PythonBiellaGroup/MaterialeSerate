# Last phase of the ETL: Load into an external source
import logging
import os

import pandas as pd

from config import ETL_CSV_ARGS, ETL_DATA_PATH, ETL_DATASET_CONFIG
from src.common.utils import check_df, get_folder_path


def save_dataset(dataframe, complete_path: str, csv_arguments={}) -> bool:

    logging.info(f"Saving dataset: {complete_path}")
    result = False
    if csv_arguments:
        args = csv_arguments.copy()
        if "engine" in args.keys():
            args.pop("engine")
            args.pop("error_bad_lines")
            args.pop("nrows")
        dataframe.to_csv(complete_path, **args)
    else:
        dataframe.to_csv(complete_path)

    result = True

    return result


def load(dataframe: pd.DataFrame) -> bool:
    logging.info("Start final loading")

    # Get the dataframes
    dataframe_list = list(dataframe.values())
    # Get the filenames from config
    dataframe_names = list(ETL_DATASET_CONFIG.values())

    # Define all the settings for the csv reading
    pandas_csv_arguments = ETL_CSV_ARGS

    folder_path = get_folder_path(".")
    data_dir = ETL_DATA_PATH
    data_path = os.path.join(folder_path, data_dir)

    # Save the files names
    file1_name = dataframe_names[0]
    file2_name = dataframe_names[1]
    file3_name = dataframe_names[2]

    file1_name = os.path.join(data_path, file1_name)
    file2_name = os.path.join(data_path, file2_name)
    file3_name = os.path.join(data_path, file3_name)

    df1 = dataframe_list[0]
    df2 = dataframe_list[1]
    df3 = dataframe_list[2]

    save_dataset(df1, file1_name, pandas_csv_arguments)
    save_dataset(df2, file2_name, pandas_csv_arguments)
    save_dataset(df3, file3_name, pandas_csv_arguments)

    return True
