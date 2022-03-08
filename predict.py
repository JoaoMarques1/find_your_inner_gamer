import joblib
import pandas as pd
from find_your_inner_gamer.params import BUCKET_NAME, MODEL_NAME
from find_your_inner_gamer.gcp import get_model_from_gcp, get_neighbors_from_gcp, get_data_from_gcp
from find_your_inner_gamer.utils import get_img


def download_model_local():
    return joblib.load('model.joblib')

def get_data_local():
    return pd.read_csv('raw_data/clean_df.csv')

def predict(game):
    df = get_data_from_gcp()
    model = get_model_from_gcp()
    X_neighbors = get_neighbors_from_gcp()
    X_neighbors.set_index('Unnamed: 0', drop=True, inplace=True)

    neighbors_index = model.kneighbors(X_neighbors.loc[[game]],n_neighbors=10)[1][0]
    neighbors_distance = model.kneighbors(X_neighbors.loc[[game]],n_neighbors=10)[0][0]
    #neighbors_list = list(neighbors_index)

    new_df_values = {
        'title' : [],
        'distance': neighbors_distance,
        'url': [],
        'price': [],
        'reviews': [],
        'op_sys': [],
        'developer': [],
        'image_url' : []
    }

    for index in neighbors_index:
        new_df_values['title'].append(df.loc[index, 'name'])
        new_df_values['url'].append(df.loc[index, 'url'])
        new_df_values['price'].append(df.loc[index, 'price'])
        new_df_values['reviews'].append(df.loc[index, 'reviews'])
        new_df_values['op_sys'].append(df.loc[index, 'op_sys'])
        new_df_values['developer'].append(df.loc[index, 'developer'])
        new_df_values['image_url'].append(get_img(df.loc[index, 'url']))
    #pd.DataFrame(neighbors_distance, index = X_neighbors.iloc[neighbors_list, :].index, columns=['distance']).head()

    recommendations = pd.DataFrame(data=new_df_values)
    recommendations.fillna('no value', inplace=True)
    return recommendations


if __name__ == "__main__":
    print(predict('DOOM'))
