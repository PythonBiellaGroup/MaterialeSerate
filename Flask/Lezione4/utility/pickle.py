import pickle
import re
from utility import checkpath


def load_pickle_file(from_path='', filename=''):
    """
    Load a pickle file to a python object (for example a model)
    """

    file_path = checkpath(from_path, filename)

    if re.search('pickle', file_path):
        try:
            pickle_in = open(file_path, "rb")
            obj = pickle.load(pickle_in)
            print(f"Pickle file loaded from: {file_path}")
            return obj

        except Exception as message:
            print(f"Impossible to read the pickle file: {message}")
            return None
    else:
        print("Please specify a path with a valid pickle file")
        return None


def create_pickle(to_path, filename, my_object):
    """
    Create a pickle file from a python object to disk
    """
    file_path = checkpath(to_path, filename)

    if re.search('pickle', file_path):
        try:

            pickle_out = open(file_path, "wb")
            pickle.dump(my_object, pickle_out)
            pickle_out.close()
            print(f"File saved correctly to: {file_path}")
            return True
        except Exception as message:
            print(f"Impossible to create the pickle file: {message}")
            return False
    else:
        print("Please specify the pickle filename correctly")
        return False
