import pandas as pd
import numpy as np
import re
import os

def get_folder_path(custom_path = '',force_creation=False):
    
    if custom_path is '' or custom_path is None:
        BASEPATH = os.path.abspath('')
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


def define_path(BASEPATH='', DATASET='test_data.xlsx',DATA_LOCATION='data', SEED=42):
    """
    Define a path for a file.
    INPUT: Basepath you want to search and dataset name plus a default location
    OUTPUT: the file path
    """
    
    #Set the random seed
    np.random.seed(SEED)
    
    if BASEPATH == '':
        BASEPATH = os.path.abspath('')
    
    #Set the default Data Path
    if DATA_LOCATION == '' or DATA_LOCATION is None:
        DATA_PATH = os.path.join(BASEPATH,DATASET)
    else:
        DATA_PATH = os.path.join(BASEPATH,DATA_LOCATION,DATASET)
    
    print(f"\n Dataset location: {DATA_PATH} \n")
    
    return DATA_PATH

def checkpath(to_path, filename):
    """
    Check path and filename
    """
    if to_path == '':
        to_path = get_folder_path('./')

    if filename == '':
        print("Please insert a valid filename")
        return None

    file_path = os.path.join(to_path, filename)

    return file_path


def define_path(BASEPATH='', DATASET='test_data.xlsx', DATA_LOCATION='', SEED=42):
    """
    Define a path for a file.
    INPUT: Basepath you want to search and dataset name plus a default location
    OUTPUT: the file path
    """

    # Set the random seed
    np.random.seed(SEED)

    if BASEPATH == '':
        BASEPATH = os.path.abspath('')

    # Set the default Data Path
    if DATA_LOCATION == '' or DATA_LOCATION is None:
        DATA_PATH = os.path.join(BASEPATH, DATASET)
    else:
        DATA_PATH = os.path.join(BASEPATH, DATA_LOCATION, DATASET)

    print(f"\n Dataset location: {DATA_PATH} \n")

    return DATA_PATH


def read_dataset_online(dataset_url, file_path='', file_name='', write_disk=False):
    try:

        file_bin = requests.get(dataset_url)

        # Write to disk
        if write_disk:
            to_path = checkpath(file_path, file_name)
            output_file = open(to_path, 'w')
            output_file.write(file_bin.text)
            output_file.close()
            print(f"File successfully writed to: {to_path}")
            return file_bin

        # Finally get the pandas dataframe
        df = pd.read_csv(dataset_url)
        print(f'File successfully readed')
        return df

    except Exception as message:
        print(f"Impossible to read the csv from url source : {message}")
        return None


def read_dataset(path='', csv_sep=',', xlsx_sheet="Sheet1", encoding='ISO-8859-1', header=0):
    """
    Read automatically a csv or xlsx file
    """
    # Check if the path is empty
    if path == '' or path == False:
        print("Please specify a path where you want to read")
        return False

    df = pd.DataFrame()

    # Load xlsx
    if re.search(r"xlsx", path):
        print("Found excel in the path")

        try:
            df = pd.read_excel(path, sheet_name=xlsx_sheet, header=header)
            print("Dataset loaded")

        except Exception as message:
            print(f"Impossibile to read xlsx: {message}")

    # Load csv
    elif re.search(r"csv", path):
        print("Found csv in the path")

        try:
            df = pd.read_csv(path, sep=csv_sep, header=header,encoding=encoding)
            print("Dataset loaded")

        except Exception as message:
            print(f"Impossibile to read csv: {message}")

    else:
        print("Impossibile to find dataset")
        return False

    return df


def save_dataset(path='', dataframe=None, csv_sep=',', index=True, header=True):
    """
    Save dataframe to disk
    """
    if dataframe is None:
        print("Please specify dataset you want to save")
        return False
    elif isinstance(dataframe, pd.DataFrame):

        # Check if the path is empty
        if path == '' or path == False:
            print("Please specify a path where you want to write")
            return False

        try:
            dataframe.to_csv(path, index=index, header=header, sep=csv_sep, encoding='utf-8')
            print(f'File saved succesfully to: {path}')
            return True
        except Exception as message:
            print(f"Impossibile to write dataframe: {message}")
            return False

    else:
        print("Please use only pandas dataframe (for now)")
        return False
