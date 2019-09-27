from app.recommenders.User_CFR import User_CFR
from app.recommenders.Evaluation import Eval
from app.recommenders.Utils import Utils
import pandas as pd


class Recommender(object):

    def __init__(self):
        self.train = pd.read_csv("data/train.csv")
        self.u = Utils(self.train)
        self.e = Eval(self.u)
        self.URM_full = self.u.URM

    def generate_result(self, recommender, path):
                return self.e.generate_predictions(recommender, path)

    def recommend_userCFR(self, knn=150, shrink=10, normalize=True, similarity='cosine', tfidf=True):
        rec = User_CFR(self.u)
        rec.fit(self.URM_full, knn, shrink, normalize, similarity, tfidf)
        return self.generate_result(rec, None)


if __name__ == '__main__':
        run = Recommender()
        run.recommend_userCFR()
