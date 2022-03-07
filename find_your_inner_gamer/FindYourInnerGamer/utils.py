from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def kmeans_labels(df, n , mi):
    vec = TfidfVectorizer(min_df = mi ,ngram_range=(1,2))
    X = vec.fit_transform(df['game_description'])
    kmodel = KMeans(n_clusters=n)
    kmodel.fit(X)

    return kmodel.labels_
