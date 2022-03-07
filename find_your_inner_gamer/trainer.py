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
from find_your_inner_gamer.data import get_data

class Trainer(object):
    def __init__(self, X, y):
        self.pipeline = None
        self.X = X
        self.y = y

    def set_pipeline(self, m=0.05, c=1, n =50, mi = 0.04):
        array_transf = FunctionTransformer(lambda array: array.toarray())
        self.X['cluster'] = kmeans_labels(self.X, n, mi)

        meta_transf = make_pipeline(
            TfidfVectorizer(min_df=m),
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

        full_pipe = make_pipeline(preproc_basic, PCA(n_components=c) )
        self.pipeline  = full_pipe.fit_transform(self.X)

    def train(self):
        X_train = pd.DataFrame(self.pipeline, index=self.X.name.tolist())
        return KNeighborsRegressor().fit(X_train, self.y)

    def save_movel(self):
        joblib.dump(self.pipeline, 'model.joblib')
        print("model.joblib saved locally", "green")


if __name__ == "__main__":
    df = get_data()
