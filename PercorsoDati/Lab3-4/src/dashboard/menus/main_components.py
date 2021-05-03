import numpy as np
import streamlit as st


def main_room_type(df):

    dataframe = df.copy()

    with st.beta_expander("Rooms", expanded=True):

        # Print the dataframe
        st.markdown("## Dataframe: Rooms")
        st.dataframe(dataframe.head(1000))

        # Types of rooms
        room_types = list(dataframe["room_type"].unique())
        st.markdown("Types of rooms")
        st.table(room_types)

        col1, col2, col3 = st.beta_columns(3)
        with col1:
            # 'listing' count per 'room_type'
            room_type_count = (
                dataframe.groupby("room_type", dropna=False)
                .id.count()
                .reset_index()
                .rename(columns={"id": "listing_count"})
            )

            st.markdown("Number of room types")
            st.dataframe(room_type_count.style.highlight_max(axis=0))

        with col2:
            # mean 'price'
            night_price = dataframe.agg({"price": [np.mean]})
            st.markdown("Mean of price")
            st.dataframe(night_price)

        with col3:
            # mean 'price' per 'room_type'
            night_price_room = dataframe.groupby("room_type").agg(
                {"price": [np.mean]}
            )
            st.markdown("Mean of price per room type")
            st.dataframe(night_price_room.style.highlight_max(axis=0))

        # mean 'price' per 'room_type'
        dataframe_resized = (
            dataframe.groupby("room_type")
            .agg({"price": ["count", "mean"]})
            .reset_index()
        )
        dataframe_resized["count_perc"] = (
            dataframe_resized["price"]["count"]
            / dataframe_resized["price"]["count"].sum()
            * 100
        )

        st.markdown("Mean of price per room type with count")
        st.dataframe(dataframe_resized.style.highlight_max(axis=0))

        # Property Type for Room Type
        pivot_df = (
            dataframe.groupby(["property_type", "room_type"])
            .price.mean()
            .round(0)
            .reset_index()
        )

        st.markdown("Property type for Room Type")
        st.dataframe(pivot_df.style.highlight_max(axis=0))
