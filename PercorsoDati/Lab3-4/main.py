from config import configure_logging
from src.launch import launch

configure_logging()

if __name__ == "__main__":
    # create the dashboard heading
    launch()