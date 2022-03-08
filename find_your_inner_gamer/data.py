import pandas as pd

def get_local_data():
    return pd.read_csv('../raw_data/clean_df.csv' )
