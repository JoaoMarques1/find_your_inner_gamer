### GCP configuration - - - - - - - - - - - - - - - - - - -


### GCP Project - - - - - - - - - - - - - - - - - - - - - -

PROJECT_ID='lewagon-bootcamp-337521'

### GCP Storage - - - - - - - - - - - - - - - - - - - - - -

BUCKET_NAME='find_your_inner_gamer'

##### Data  - - - - - - - - - - - - - - - - - - - - - - - -
BUCKET_CSV_DATA_PATH="data/clean_df.csv"
BUCKET_TRANSFORMED_CSV_DATA_PATH= "data/X_neighbors.csv"

# train data file location
# /!\ here you need to decide if you are going to train using the provided and uploaded data/train_1k.csv sample file
# or if you want to use the full dataset (you need need to upload it first of course)
BUCKET_LOCAL_DATA_PATH = '../raw_data/clean_df.csv'

##### Training  - - - - - - - - - - - - - - - - - - - - - -

# not required here

##### Model - - - - - - - - - - - - - - - - - - - - - - - -

# model folder name (will contain the folders for all trained model versions)
MODEL_NAME = 'inner_gamer'

# model version folder name (where the trained model.joblib file will be stored)
MODEL_VERSION = 'v1'

### GCP AI Platform - - - - - - - - - - - - - - - - - - - -

# not required here

### - - - - - - - - - - - - - - - - - - - - - - - - - - - -
