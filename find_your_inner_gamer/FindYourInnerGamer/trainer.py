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
        X_train = pd.DataFrame(self.pipeline, index=self.X.name.tolist())
        return KNeighborsRegressor().fit(X_train, self.y)

    def save_movel(self):
        joblib.dump(self.pipeline, 'model.joblib')
        print("model.joblib saved locally", "green")


if __name__ == "__main__":
    df = get_data()
    df = get_data_from_gcp()
    df = clean_data(df)
    y = df["fare_amount"]
    X = df.drop("fare_amount", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # Train and save model, locally and
    trainer = Trainer(X=X_train, y=y_train)
    trainer.set_experiment_name('xp2')
    trainer.run()
    rmse = trainer.evaluate(X_test, y_test)
    print(f"rmse: {rmse}")
    trainer.save_model_locally()
    storage_upload()
