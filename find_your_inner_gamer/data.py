from distutils.command.clean import clean
import pandas as pd

def get_data():
    return pd.read_csv('../raw_data/clean_df.csv')


### merge with review csv + date csv + price csv
### replace na by english in languages


### merge genre and popular tag in one column
### drop columns :publisher, all_rveiews, recent_reviews, discount, genre, popular tags
 


##replace na in other columns
