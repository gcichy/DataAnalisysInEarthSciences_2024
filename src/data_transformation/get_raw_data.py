import os


def get_raw_data_dir():
    """
    Function gets location where raw data is stored
    """
    return os.path.join(os.path.dirname(__file__), '..','..','data','raw')

