import os

import streamlit as st
import pandas as pd
from app.src.common.config import DATA_PATH


@st.cache(persist=True, show_spinner=True, suppress_st_warning=True)
def read_dataframe():

    data_path = os.path.join(DATA_PATH, "tweet_cleaned.csv")
    df = pd.read_csv(data_path, sep="|")

    return df
