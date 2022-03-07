import pandas as pd
import numpy as np
import joblib

from sklearn.decomposition import PCA
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import RobustScaler, StandardScaler, OneHotEncoder
from sklearn.preprocessing import FunctionTransformer

from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

from find_your_inner_gamer.utils import kmeans_labels
from find_your_inner_gamer.data import get_data, get_data_from_gcp
from find_your_inner_gamer.gcp  import data_upload, storage_upload

class Trainer(object):
    def __init__(self, X, y, X_neighbors):
        self.pipeline = None
        self.X = X
        self.y = y
        self.X_neighbors = X_neighbors

    def set_pipeline(self):
        array_transf = FunctionTransformer(lambda array: array.toarray())
        self.X['cluster'] = kmeans_labels(self.X)

        meta_transf = make_pipeline(
            TfidfVectorizer(min_df=0.03),
            array_transf,
            RobustScaler()
        )

        ord_encoder = OrdinalEncoder(
            categories=[
                [
                    "Overwhelmingly Negative",
                    "Very Negative",
                    "Negative",
                    "Mostly Negative",
                    'Mixed',
                    "Mostly Positive",
                    "Positive",
                    "Very Positive",
                    "Overwhelmingly Positive"
                ]],
            dtype=np.int64,
            handle_unknown="use_encoded_value",
            unknown_value=-1
        )

        ord_transf = make_pipeline(
        ord_encoder,
        StandardScaler())

        cluster_transf = make_pipeline(
            OneHotEncoder(sparse=False),
            StandardScaler()
        )

        num_transf = make_pipeline(StandardScaler())


        preproc_basic = make_column_transformer(
            (meta_transf, 'metadata'),
            (cluster_transf, ['cluster']),
            (ord_transf, ['reviews']),
            (num_transf, ['mature_content', 'achievements']),
            remainder='drop'
        )

        full_pipe = make_pipeline(preproc_basic, PCA(n_components=10) )
        self.pipeline  = full_pipe.fit_transform(self.X)

    def train(self):
        self.X_neighbors = pd.DataFrame(self.pipeline, index=self.X.name.tolist())
        return KNeighborsRegressor().fit(self.X_neighbors, self.y)

    def save_model(self):
        joblib.dump(self.pipeline, 'model.joblib')
        print("model.joblib saved locally")

    def save_dataframe(self):
        self.X_neighbors.to_csv('../raw_data/X_neighbors.csv', index=False)



if __name__ == "__main__":
    df = get_data_from_gcp()

    # Train and save model, locally and
    trainer = Trainer()
    trainer.set_pipeline()
    trainer.train()
    trainer.save_model()
    trainer.save_dataframe()

    storage_upload()
    data_upload()
