import pandas as pd
from google.cloud import storage
from find_your_inner_gamer.params import BUCKET_NAME,BUCKET_CSV_DATA_PATH

def get_data():
    return pd.read_csv('../raw_data/clean_df.csv' )

def get_data_from_gcp(optimize=False, **kwargs):
    """method to get the data from google cloud bucket"""
    # Add Client() here
    client = storage.Client()
    path = f"gs://{BUCKET_NAME}/{BUCKET_CSV_DATA_PATH}"
    df = pd.read_csv(path)
    return df
