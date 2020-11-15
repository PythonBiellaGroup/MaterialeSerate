import re
import os
import yaml


def get_folder_path(custom_path="", force_creation=False):

    if custom_path is "" or custom_path is None:
        BASEPATH = os.path.abspath("")
    else:
        BASEPATH = os.path.abspath(custom_path)

    # Check if the folder exist, if not exit you can create with a flag
    if not os.path.exists(BASEPATH):
        print("WARNING: Path doesn't exist")
        if force_creation:
            print("Force creation folder")
            try:
                os.makedirs(BASEPATH)
            except Exception as message:
                print(f"Impossible to create the folder: {message}")

    print(f"PATH: {BASEPATH}, force creation: {force_creation}")
    return BASEPATH


def define_path(BASEPATH="", DATASET="test_data.xlsx", DATA_LOCATION="data", SEED=42):
    """
    Define a path for a file.
    INPUT: Basepath you want to search and dataset name plus a default location
    OUTPUT: the file path
    """

    # Set the random seed
    np.random.seed(SEED)

    if BASEPATH == "":
        BASEPATH = os.path.abspath("")

    # Set the default Data Path
    if DATA_LOCATION == "" or DATA_LOCATION is None:
        DATA_PATH = os.path.join(BASEPATH, DATASET)
    else:
        DATA_PATH = os.path.join(BASEPATH, DATA_LOCATION, DATASET)

    print(f"\n Dataset location: {DATA_PATH} \n")

    return DATA_PATH


def checkpath(to_path, filename):
    """
    Check path and filename
    """
    if to_path == "":
        to_path = get_folder_path("./")

    if filename == "":
        print("Please insert a valid filename")
        return None

    file_path = os.path.join(to_path, filename)

    return file_path


def define_path(BASEPATH="", DATASET="test_data.xlsx", DATA_LOCATION="data", SEED=42):
    """
    Define a path for a file.
    INPUT: Basepath you want to search and dataset name plus a default location
    OUTPUT: the file path
    """

    # Set the random seed
    np.random.seed(SEED)

    if BASEPATH == "":
        BASEPATH = os.path.abspath("")

    # Set the default Data Path
    if DATA_LOCATION == "" or DATA_LOCATION is None:
        DATA_PATH = os.path.join(BASEPATH, DATASET)
    else:
        DATA_PATH = os.path.join(BASEPATH, DATA_LOCATION, DATASET)

    print(f"\n Dataset location: {DATA_PATH} \n")

    return DATA_PATH


def read_yaml_file(file_path, filename=""):
    """
    Read a yaml file from disk
    """
    file_path = checkpath(file_path, filename)

    try:
        with open(file_path, "r") as file:

            data = yaml.safe_load(file)
            file.close()
        print(f"File succesfully readed")
        return data

    except Exception as message:
        print(f"Impossibile to read the file: {message}")
        return None


def write_dataset_yaml(to_path="", filename="", dataset=None):
    """
    Write a pandas dataset to yaml
    """
    file_path = checkpath(to_path, filename)

    if isinstance(dataset, pd.DataFrame) == False:
        print(f"Please use a Pandas dataframe with write_dataset_yaml function")
        return False

    try:
        with open(file_path, "w") as file:
            documents = yaml.dump(dataset, file)
        file.close()
        print(f"File succesfully writed to: {file_path}")
        return True

    except Exception as message:
        print(f"Impossibile to write the file: {message}")
        return False


def write_yaml(to_path, filename, things):
    """
    Write some properties to generic yaml file
    """
    file_path = checkpath(to_path, filename)

    try:
        with open(file_path, "w") as file:
            documents = yaml.dump(things, file)
        file.close()
        print(f"File succesfully writed to: {file_path}")
        return True

    except Exception as message:
        print(f"Impossibile to write the file: {message}")
        return False
