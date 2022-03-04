import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import FunctionTransformer

from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import RobustScaler, StandardScaler

def create_pipeline(df):
    array_transf = FunctionTransformer(lambda array: array.toarray())

    meta_transf = make_pipeline(TfidfVectorizer(min_df=0.05), array_transf,RobustScaler())
    desc_transf = make_pipeline(TfidfVectorizer(min_df=0.1),array_transf, RobustScaler())

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

    ord_transf = make_pipeline(ord_encoder, StandardScaler())
    num_transf = make_pipeline(StandardScaler())

    preproc_basic = make_column_transformer(
        (meta_transf, 'metadata'),
        #(meta_transf, 'game_description'),
        (ord_transf, ['reviews']),
        #(num_transf, ['mature_content', 'achievements']),
        remainder='drop'
    )

    return preproc_basic.fit_transform(df)
