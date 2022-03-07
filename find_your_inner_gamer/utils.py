from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import requests
from bs4 import BeautifulSoup

def kmeans_labels(df):
    vec = TfidfVectorizer(min_df = 0.07 ,ngram_range=(1,2))
    X = vec.fit_transform(df['game_description'])
    kmodel = KMeans(n_clusters=70)
    kmodel.fit(X)

    return kmodel.labels_


def get_img(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    try:
        return soup.find('img', class_='game_header_image_full').attrs['src']
    except AttributeError:
        return 'no image'
