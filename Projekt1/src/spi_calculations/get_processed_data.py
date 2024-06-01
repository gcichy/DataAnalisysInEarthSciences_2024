import pandas as pd
import os

def get_processed_data():
    """
    Function gets location where raw data is stored
    """
    path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'processed_data.csv')
    df = pd.read_csv(path)
    return df

#get_raw_data_dir()