from app.recommenders.User_CFR import User_CFR
from app.recommenders.Evaluation import Eval
from app.recommenders.Utils import Utils
import pandas as pd


class Recommender(object):

    def __init__(self):
        self.train = pd.read_csv("../data/train.csv")
        self.u = Utils(self.train)
        self.e = Eval(self.u)
        self.URM_full = self.u.URM

    def generate_result(self, recommender, path, target_receipt):
                return self.e.generate_predictions(recommender, path, target_receipt)

    def recommend_userCFR(self, knn=150, shrink=10, normalize=True, similarity='cosine', tfidf=True, target_receipt=None):
        rec = User_CFR(self.u)
        rec.fit(self.URM_full, knn, shrink, normalize, similarity, tfidf)
        return self.generate_result(rec, None, target_receipt)


if __name__ == '__main__':

        target_receipt = 10

        run = Recommender()
        run.recommend_userCFR(target_receipt=target_receipt)
