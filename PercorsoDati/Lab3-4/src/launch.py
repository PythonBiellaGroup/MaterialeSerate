import logging
import streamlit as st

from src.preprocessing.process import import_data
from src.dashboard.menu import main_menu, side_menu


def launch():
    """Main function to launch all the streamlit functionalities

    Returns:
        bool: True if the process is ok, False if there are some errors
    """

    logging.info("Starting streamlit program")

    # Streamlit page settings
    st.set_page_config(
        layout="wide",
        page_title="PythonBiellaGroup Dashboard",
        page_icon="🧊",
        initial_sidebar_state="expanded",
    )

    # Import Data
    datasets = import_data()

    # Deserialize object
    data = list(datasets.values())
    listings = data[0]
    # reviews = data[1]
    # calendar = data[2]

    # Launch the side menu for all the configurations
    main_menu()

    side_menu(listings)

    return True