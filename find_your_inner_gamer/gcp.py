import os

from google.cloud import storage
from termcolor import colored
from find_your_inner_gamer.params import BUCKET_NAME, MODEL_NAME, MODEL_VERSION


def storage_upload(rm=False):
    client = storage.Client().bucket(BUCKET_NAME)

    local_model_name = 'model.joblib'
    storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename('model.joblib')
    print(colored(f"=> model.joblib uploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  "green"))
    if rm:
        os.remove('model.joblib')


def data_upload(rm=False):
    client = storage.Client().bucket(BUCKET_NAME)

    local_model_name = 'X_DataFrame.csv'
    storage_location = f"Data/{local_model_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename('X_DataFrame.csv')
    print(colored(f"=> X_DataFrame.csvuploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  ))
    if rm:
        os.remove('X_DataFrame.csv')
