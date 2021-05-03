# Second phase of ETL: Transformations on the data
import logging

import pandas as pd

from config import ETL_EXTRACTION_CONFIG
from etl.utils import remove_dollar
from etl.extract import import_data


def tf_listings(filename: str, dataframe: pd.DataFrame) -> pd.DataFrame:

    # Keep only some columns
    listings = dataframe[
        [
            "id",
            "name",
            "longitude",
            "latitude",
            "listing_url",
            "instant_bookable",
            "host_response_time",
            "review_scores_rating",
            "property_type",
            "room_type",
            "accommodates",
            "bathrooms",
            "bedrooms",
            "beds",
            "reviews_per_month",
            "amenities",
            "number_of_reviews",
            "price",
        ]
    ]
    # Remove the dollars
    listings = listings.assign(price=remove_dollar(listings.price))
    listings[["price"]]

    return listings


def tf_reviews(filename: str, dataframe: pd.DataFrame) -> pd.DataFrame:

    # Date to datetime
    reviews = dataframe.assign(date=pd.to_datetime(dataframe["date"]))

    # Create month and year new columns
    reviews["year"] = reviews["date"].dt.year
    reviews["month"] = reviews["date"].dt.month
    reviews = reviews.sort_values(["year", "month"], ascending=False)

    return reviews


def tf_calendar(filename: str, dataframe: pd.DataFrame):

    # Create date from datetime
    calendar = dataframe.assign(date=pd.to_datetime(dataframe["date"]))
    # Adjust the price
    calendar = calendar.assign(
        price=pd.to_numeric(
            calendar.price.str.replace("$", "").str.replace(",", "")
        ),
    )
    # Define year and month
    calendar["year"] = pd.DatetimeIndex(calendar["date"]).year
    calendar["month"] = pd.DatetimeIndex(calendar["date"]).month

    calendar = calendar.sort_values(["year", "month"], ascending=False)

    # Map logic values
    calendar["available"] = calendar.available.map({"t": True, "f": False})

    return calendar


def transform(dataframes: dict) -> pd.DataFrame:
    logging.info("Start transformations")

    if dataframes is None:
        logging.info("Input dataset not loaded, try to reload it")
        dataframes = import_data(remote=False, config=ETL_EXTRACTION_CONFIG)

    # Get the names of the tables
    list_tables = list(dataframes.keys())
    # Get the pandas dataframes
    list_dataframe = list(dataframes.values())

    file1 = list_dataframe[0]
    file2 = list_dataframe[1]
    file3 = list_dataframe[2]

    file1_name = list_tables[0]
    file2_name = list_tables[1]
    file3_name = list_tables[2]

    logging.info(f"Start transforming {file1_name} file")
    listings = tf_listings(file1_name, file1)

    logging.info(f"Start transforming {file2_name} file")
    reviews = tf_reviews(file2_name, file2)

    logging.info(f"Start transforming {file3_name} file")
    calendar = tf_calendar(file3_name, file3)

    # Compose the dictionary and return
    datasets = {
        file1_name: listings,
        file2_name: reviews,
        file3_name: calendar,
    }

    return datasets