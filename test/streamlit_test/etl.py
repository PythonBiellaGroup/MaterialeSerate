import logging

from etl.extract import import_data
from etl.transform import transform
from etl.load import load

# from etl.load import

if __name__ == "__main__":
    # create the dashboard heading
    logging.info("Launching ETL")

    dataset = None
    # Extract and import data from remote repo
    # dataset = import_data(remote=True)
    # Transform data
    dataset = transform(dataset)
    # Save data to disk
    result = load(dataset)

    logging.info(f"ETL finished: {result}")