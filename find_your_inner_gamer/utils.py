from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def kmeans_labels(df):
    vec = TfidfVectorizer(min_df = 0.07 ,ngram_range=(1,2))
    X = vec.fit_transform(df['game_description'])
    kmodel = KMeans(n_clusters=70)
    kmodel.fit(X)

    return kmodel.labels_
