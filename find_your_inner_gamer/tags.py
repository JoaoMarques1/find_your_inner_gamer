import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_tags(url):
    """
    Scrapes the url website for the game tags

    Args:
        url (str): Link to the web page for a given game

    Returns:
        str/float: review category or if missing 'NaN' value.
    """
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    try:
        return ','.join([tag.text.strip() for tag in soup.find_all('a', class_='app_tag')])
    except:
        return float('nan')


def clean_tags(tag):
    """
    keep only one unique value of the tags per game

    Args:
        tag : game tag

    Returns:
        str of tags separated by a coma
    """
    if ',' in str(tag):
        tag = ','.join(list(set(str(tag).split(','))))
        return tag


def tag_list(df):
    """
    Making a list of the 20 most frequent tags

    Args:
        df : our dataframe

    Returns:
        list of tags
    """

    tags = {}
    # Stripping game details
    df.tags= df.tags.str.strip()
    for index, row in df.iterrows():
        tags_list= str(row['tags']).split(',')
        for tag in tags_list:
            if not tag in tags:
                tags[tag] = 1
            else:
                tags[tag] += 1

    tags_df = pd.DataFrame(list(tags.items()),columns = ['tags','count'])
    tag_list = [tag for tag in tags_df.sort_values('count', ascending =False).head(20)['tags']]

    return tag_list
