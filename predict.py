import os

import joblib
import pandas as pd
from find_your_inner_gamer.params import BUCKET_NAME, MODEL_NAME
from google.cloud import storage


# PATH_TO_LOCAL_MODEL = 'model.joblib'

# AWS_BUCKET_TEST_PATH = "s3://wagon-public-datasets/taxi-fare-test.csv"





def download_model(model_directory="PipelineTest", bucket=BUCKET_NAME, rm=True):
    client = storage.Client().bucket(bucket)

    storage_location = 'models/{}/versions/{}/{}'.format(
        MODEL_NAME,
        model_directory,
        'model.joblib')
    blob = client.blob(storage_location)
    blob.download_to_filename('model.joblib')
    print("=> pipeline downloaded from storage")
    model = joblib.load('model.joblib')
    if rm:
        os.remove('model.joblib')
    return model


def get_model(path_to_joblib):
    pipeline = joblib.load(path_to_joblib)
    return pipeline

def recommending_system(model, X, game):

    neighbors_index = model.kneighbors(X.loc[[game]],n_neighbors=df.shape[0])[1][0]
    neighbors_distance = model.kneighbors(X.loc[[game]],n_neighbors=df.shape[0])[0][0]

    neighbors_list = list(neighbors_index)
    # new_df_values = {
    #     'distance': neighbors_distance,
    #     'url': [],
    #     'price': [],
    #     'reviews': [],
    #     'op_sys': [],
    #     'developer': [],
    # }
    # for index in neighbors_index:
    #     new_df_values['url'].append(df.loc[index, 'url'])
    #     new_df_values['price'].append(df.loc[index, 'price'])
    #     new_df_values['reviews'].append(df.loc[index, 'reviews'])
    #     new_df_values['op_sys'].append(df.loc[index, 'op_sys'])
    #     new_df_values['developer'].append(df.loc[index, 'developer'])

    return pd.DataFrame(neighbors_distance, index = X.iloc[neighbors_list, :].index, columns=['distance'])



if __name__ == '__main__':

    #TODO recommending_system(download_model(), download_path)
