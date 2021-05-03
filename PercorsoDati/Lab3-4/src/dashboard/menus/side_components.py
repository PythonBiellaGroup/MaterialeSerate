import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotnine as pn


from src.dashboard.menus.main_components import main_room_type
from src.common.dashboard import get_table_download_link
from src.common.utils import get_folder_path


def visualize_dataset(dataframe: pd.DataFrame) -> bool:

    button = st.sidebar.button(
        "Visualize dataframe without filters", key="bvisualize"
    )

    if button:
        main_room_type(dataframe)
        return True

    return False


def search_room(dataframe: pd.DataFrame) -> bool:

    # Search top 100
    top100 = st.sidebar.checkbox(
        "Filter top 100 apartments",
        help="filter only the top 100 apartments by price",
    )

    # Search by price
    min_price, max_price = st.sidebar.slider(
        "Search apartments by price",
        min(dataframe.price),
        max(dataframe.price),
        (min(dataframe.price), max(dataframe.price)),
        help="Insert the min and max price",
    )

    # Search by review_scores_rating

    # Search by room type

    # Search by Beds

    # Search by Beds

    # Search by Bathrooms

    # Search by Accomodates

    # Select columns for plot
    to_select = st.sidebar.multiselect(
        "Seleziona le colonne che vuoi visualizzare",
        list(dataframe.columns),
        [i for i in list(dataframe.columns)],
        help="Seleziona le colonne che vuoi considerare",
    )

    if top100:
        dataframe = dataframe.groupby("price").head(100)

    dataframe_filtered = dataframe[to_select]

    dataframe_filtered = dataframe_filtered.loc[
        dataframe.price.between(min_price, max_price)
    ]
    # Launch the data visualization
    main_room_type(dataframe_filtered)

    st.sidebar.markdown("Select plot axis")
    axis1 = st.sidebar.selectbox(
        "Select first axis", list(dataframe_filtered.columns)
    )
    axis2 = st.sidebar.selectbox(
        "Select second axis", list(dataframe_filtered.columns)
    )

    scatterplot = st.sidebar.button(
        "Scatterplot", key="bscatterplot", help="Launch the scatterplot"
    )
    if scatterplot:
        fig = px.scatter(dataframe_filtered, x=axis1, y=axis2)
        st.markdown(f"Plot with: {axis1}, {axis2}")
        st.plotly_chart(fig)
        st.markdown("Raw data used")

        st.dataframe(
            dataframe_filtered.style.highlight_max(axis=0)
            .format({axis2: "{:.2%}"})
            .highlight_null(null_color="red")
            .set_caption("Result table with all the data filtered")
        )
        return True

    barplot = st.sidebar.button(
        "Barplot", key="bggplot", help="Launch the ggplot"
    )
    if barplot:

        st.markdown(
            "To launch this plot please remember to select all the columns in the data"
        )
        # plot_folder_path = os.path.join(get_folder_path("."), "plots")

        fig = (
            pn.ggplot(dataframe_filtered)
            + pn.aes(x=axis1, fill=axis2)
            + pn.geom_bar()
            + pn.theme(axis_text_x=pn.element_text(angle=45, hjust=1))
        )

        st.markdown("### Barplot")
        st.markdown(f"Displaying: {axis1} over {axis2}")
        st.pyplot(
            pn.ggplot.draw(fig),
            clear_figure=True,
            width=100,
            height=200,
            dpi=600,
        )
        # st.image(fig_path)
        # st.write(fig)

        # st.pyplot(fig)

    histogram = st.sidebar.button(
        "Histogram", key="bp9histogram", help="Launch the ggplot histogram"
    )
    if histogram:
        fig = (
            pn.ggplot(dataframe_filtered)
            + pn.aes(x="price")
            + pn.geom_histogram(fill="blue", colour="black", bins=30)
            + pn.xlim(0, 200)
        )

        st.markdown("### Histogram")
        st.markdown(f"Displaying: {axis1} over {axis2}")
        st.pyplot(
            pn.ggplot.draw(fig),
            clear_figure=True,
            width=100,
            height=200,
            dpi=600,
        )

    density = st.sidebar.button(
        "Density", key="bp9density", help="Launch the ggplot density"
    )
    if density:

        fig = (
            pn.ggplot(dataframe_filtered.head(1000))
            + pn.aes(x="price")
            + pn.geom_density(fill="blue", colour="black", alpha=0.5)
            + pn.xlim(0, 200)
        )

        st.markdown("### Density Plot")
        st.pyplot(
            pn.ggplot.draw(fig),
            clear_figure=True,
            width=100,
            height=200,
            dpi=600,
        )

    latlong = st.sidebar.button(
        "Latitude-Longitude",
        key="bp9latlon",
        help="Launch the ggplot latitude and longitude categorical comparison",
    )
    if latlong:
        # color categorical variable
        fig = (
            pn.ggplot(
                dataframe_filtered,
                pn.aes(x="latitude", y="longitude", colour="room_type"),
            )
            + pn.geom_point(alpha=0.5)
        )

        st.markdown("### Color categorical variable")
        st.pyplot(
            pn.ggplot.draw(fig),
            clear_figure=True,
            width=100,
            height=200,
            dpi=600,
        )

        return True

    return False


def download_data(dataframe):
    button = st.sidebar.button("Download data", key="bdownload")
    excel_check = st.sidebar.checkbox(
        "Do you want to download an excel?",
        False,
        help="Press this checkbox if you want to download an excel",
    )
    if button:
        with st.beta_expander("Download data", expanded=True):
            st.markdown(
                get_table_download_link(dataframe, excel_check),
                unsafe_allow_html=True,
            )
        return True

    return False