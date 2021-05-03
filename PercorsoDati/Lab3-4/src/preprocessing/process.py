import os
import logging

import pandas as pd
import streamlit as st

from config import APP_DATASET_CONFIG, APP_CSV_ARGS, APP_DATA_PATH
from src.common.utils import get_folder_path, check_df


# Read dataset simple
@st.cache(persist=True, show_spinner=True, suppress_st_warning=True)
def read_dataset(complete_path: str, csv_arguments={}) -> pd.DataFrame:
    if csv_arguments:
        dataframe = pd.read_csv(complete_path, **csv_arguments)
    else:
        dataframe = pd.read_csv(complete_path)

    return dataframe


# Import data extract main function
@st.cache(persist=True, show_spinner=True, suppress_st_warning=True)
def import_data(config=APP_DATASET_CONFIG) -> dict:
    logging.info("Start importing the data")
    with st.spinner("Importing the data..."):
        # Get the dataframe names
        dataframe_names = list(config.keys())
        # Get the filenames from config
        data_files = list(config.values())

        # Define all the settings for the csv reading
        pandas_csv_arguments = APP_CSV_ARGS

        folder_path = get_folder_path(".")
        data_dir = APP_DATA_PATH
        data_path = os.path.join(folder_path, data_dir)
        # Define the folder data path

        datasets = {}
        for i, file_name in enumerate(data_files):
            dataframe = read_dataset(
                os.path.join(data_path, file_name), pandas_csv_arguments
            )
            datasets[dataframe_names[i]] = dataframe
            check_df(dataframe)

    st.success("Data loaded successfully!")
    return datasets