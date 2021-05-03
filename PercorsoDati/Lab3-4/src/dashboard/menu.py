import logging

import streamlit as st

from src.dashboard.menus.side_components import (
    visualize_dataset,
    search_room,
    download_data,
)


def side_menu(dataframe):
    """
    Streamlit side config menu
    """
    logging.debug("Launching side menù function")

    st.sidebar.markdown("**Configuration Panel**")

    #### FILTER DATA ####
    visualize_dataset(dataframe)
    search_room(dataframe)

    #### DOWNLOAD DATA ####
    download_data(dataframe)


def main_menu():

    logging.debug("Launching main menu")
    st.markdown(
        f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: 1400px;
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )
    # create the dashboard heading
    st.title("Python Biella Group")
    st.markdown("## Streamlit project example")
    st.markdown("How to use streamlit for your Data Project")
    st.markdown("<-- Open side menu to filter the data")

    return True
