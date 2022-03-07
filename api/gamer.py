from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import joblib
from find_your_inner_gamer.image import get_img
from find_your_inner_gamer.data import get_data_from_gcp, get_model_from_gcp,get_X_data_from_gcp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict")

def predict(game):

    model = get_model_from_gcp()
    X_neighbors = get_X_data_from_gcp()
    df = get_data_from_gcp()

    neighbors_index = model.kneighbors(X_neighbors.loc[[game]],n_neighbors=10)[1][0]
    neighbors_distance = model.kneighbors(X_neighbors.loc[[game]],n_neighbors=10)[0][0]

    neighbors_list = list(neighbors_index)
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
    new_df_values['title'] = neighbors_list
    for index in neighbors_index:
         new_df_values['title'].append(df.loc[index, 'name'])
         new_df_values['url'].append(df.loc[index, 'url'])
         new_df_values['price'].append(df.loc[index, 'price'])
         new_df_values['reviews'].append(df.loc[index, 'reviews'])
         new_df_values['op_sys'].append(df.loc[index, 'op_sys'])
         new_df_values['developer'].append(df.loc[index, 'developer'])
         new_df_values['image_url'].append(get_img(df.loc[index, 'url']))

    #pd.DataFrame(neighbors_distance, index = X_neighbors.iloc[neighbors_list, :].index, columns=['distance']).head()

    return new_df_values
