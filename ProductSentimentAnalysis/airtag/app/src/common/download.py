import streamlit as st
import pandas as pd


@st.cache
def convert_df(df: pd.DataFrame):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")
