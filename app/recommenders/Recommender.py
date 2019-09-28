from app.recommenders.User_CFR import User_CFR
from app.recommenders.Item_CFR import Item_CFR
from app.utils.Evaluation import Eval
from app.utils.Utils import Utils
import pandas as pd
import numpy as np
import scipy.sparse as sp
import csv
import os


class Recommender(object):

    def __init__(self):
        try:
            self.train = pd.read_csv("app/data/train.csv")
        except FileNotFoundError:
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

    def recommend_itemCFR(self, knn=150, shrink=10, normalize=True, similarity='cosine', tfidf=True, target_receipt=None):
        rec = Item_CFR(self.u)
        rec.fit(self.URM_full, knn, shrink, normalize, similarity, tfidf)
        return self.generate_result(rec, None, self.toSparse(target_receipt))

    def update_matrices(self):
        self.u = Utils(self.train)
        self.e = Eval(self.u)
        self.URM_full = self.u.URM
        os.remove("../data/item_sim.npz")
        return print("URM updated and similarity matrix file deleted")

    @staticmethod
    def append_receipt(receipt_id, receipt_content):
        with open('../data/train.csv', 'a') as fd:
            file_writer = csv.writer(fd)
            for item in receipt_content:
                file_writer.writerow([receipt_id, item])
        return

    def toSparse(self, data):
        # row indices
        data_l = len(data)
        row_ind = np.zeros(data_l, dtype=int)
        # column indices
        col_ind = np.array(data)
        # data to be stored in COO sparse matrix
        data = np.ones(data_l, dtype=int)

        mat_coo = sp.coo_matrix((data, (row_ind, col_ind)))
        target_receipt = mat_coo.tocsr()
        #return target_receipt
        target_receipt = sp.csr_matrix((data, (row_ind, col_ind)), shape=(1, 24))
        return target_receipt


if __name__ == '__main__':

        data = [10,18]

        run = Recommender()
        result = run.recommend_itemCFR(target_receipt=data)
        print(result)
