from find_your_inner_gamer.data import get_data
from find_your_inner_gamer.pipeline import create_pipeline
from sklearn.neighbors import KNeighborsRegressor
import joblib

class Trainer(object):
    def __init__(self, X, y):
        self.pipe = None
        self.X = X
        self.y = y


    def set_pipeline(self):
        self.pipe = create_pipeline(self.X)

    def train(self):
        self.pipe = KNeighborsRegressor().fit(self.X, self.y)

    def save_model(self):
        joblib.dump(self.pipe, 'model.joblib')


if __name__ == '__main__':
    # Get and clean data
    df = get_data()
    # Train and save model
