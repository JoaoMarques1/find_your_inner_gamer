import pandas as pd
from google.cloud import storage
import joblib
from find_your_inner_gamer.params import BUCKET_NAME, BUCKET_CSV_DATA_PATH,BUCKET_TRANSFORMED_CSV_DATA_PATH,MODEL_NAME, MODEL_VERSION


def get_local_data():
    return pd.read_csv('../raw_data/clean_df.csv' )

def get_clean_data_from_gcp():
    """method to get the  data from google cloud bucket"""
    # Add Client() here
    client = storage.Client()
    path = f"gs://{BUCKET_NAME}/{BUCKET_CSV_DATA_PATH}"
    df = pd.read_csv(path)
    return df

def get_X_data_from_gcp():
    """method to get the  data from google cloud bucket"""
    # Add Client() here
    client = storage.Client()
    path = f"gs://{BUCKET_NAME}/{BUCKET_TRANSFORMED_CSV_DATA_PATH}"
    df = pd.read_csv(path)
    return df

def get_model_from_gcp():
    """method to get the model from google cloud bucket"""
    client = storage.Client().bucket(BUCKET_NAME)
    local_model_name = 'model.joblib'
    storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    blob = client.blob(storage_location)
    blob.download_to_filename('model.joblib')
    model = joblib.load('model.joblib')
    return model
