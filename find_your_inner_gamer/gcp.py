import os
import pandas as pd
import joblib

from google.cloud import storage
from find_your_inner_gamer.params import BUCKET_NAME, BUCKET_CSV_DATA_PATH,MODEL_NAME, MODEL_VERSION


def get_data_from_gcp():
    """method to get the  data from google cloud bucket"""
    # Add Client() here
    client = storage.Client()
    path = f"gs://{BUCKET_NAME}/{BUCKET_CSV_DATA_PATH}"
    df = pd.read_csv(path)
    return df


def get_neighbors_from_gcp():
    """method to get the  data from google cloud bucket"""
    # Add Client() here

    path = f"gs://{BUCKET_NAME}/data/X_neighbors.csv"
    df = pd.read_csv(path)
    return df


def get_model_from_gcp():
    """method to get the  data from google cloud bucket"""
    # Add Client() here
    client = storage.Client().bucket(BUCKET_NAME)

    local_model_name = 'model.joblib'
    model_storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    blob = client.blob(model_storage_location)
    blob.download_to_filename('model.joblib')
    model = joblib.load('model.joblib')
    return model


def storage_upload(rm=True):
    client = storage.Client().bucket(BUCKET_NAME)

    local_model_name = 'model.joblib'
    model_storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    blob = client.blob(model_storage_location)
    blob.upload_from_filename('model.joblib')
    print(f"=> model.joblib uploaded to bucket {BUCKET_NAME} inside {model_storage_location}")

    local_neighbors_csv = 'X_neighbors.csv'
    neighbors_storage_location = f"data/{local_neighbors_csv}"
    blob = client.blob(neighbors_storage_location)
    blob.upload_from_filename('X_neighbors.csv')
    print(f"=> X_neighbors.csv uploaded to bucket {BUCKET_NAME} inside {neighbors_storage_location}")

    if rm:
        os.remove('model.joblib')
        os.remove('X_neighbors.csv')
