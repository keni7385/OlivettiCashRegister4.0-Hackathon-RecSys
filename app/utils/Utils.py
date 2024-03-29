import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import TfidfTransformer


class Utils(object):

    def __init__(self, train):
        self.train = train
        self.URM = self.build_URM()

    @staticmethod
    def get_top_3(URM, target_playlist, row):
        #my_songs = URM.indices[URM.indptr[target_playlist]:URM.indptr[target_playlist + 1]]

        # from sparse to dense to filter items already present in the list
        target_playlist = target_playlist.todense()

        row[np.squeeze(np.asarray(target_playlist == 1))] = -np.inf
        #row[my_songs] = -np.inf



        relevant_items_partition = (-row).argpartition(3)[0:3]
        relevant_items_partition_sorting = np.argsort(-row[relevant_items_partition])
        ranking = relevant_items_partition[relevant_items_partition_sorting]
        return ranking

    @staticmethod
    def get_similarity(matrix, knn, shrink, normalize, similarity):
        from app.recommenders.cython.Compute_Similarity_Cython import \
            Compute_Similarity_Cython as Cython_Cosine_Similarity

        similarity = Cython_Cosine_Similarity(matrix, normalize=normalize, shrink=shrink, similarity=similarity,
                                              topK=knn)
        return similarity.compute_similarity().tocsr()

    @staticmethod
    def get_UCM(URM, tfidf):
        if not tfidf:
            return URM
        else:
            UCM = TfidfTransformer().fit_transform(URM.T).T
            return UCM

    def build_URM(self):
        user_list = self.train.playlist_id.values
        item_list = self.train.track_id.values
        rating_list = np.ones(len(user_list))
        URM = sp.coo_matrix((rating_list, (user_list, item_list)))

        return URM.tocsr()

    def get_usersim_CF(self, URM, knn, shrink, normalize=True, similarity='cosine', tfidf=True):
        UCM = self.get_UCM(URM.T, tfidf)
        return self.get_similarity(UCM, knn, shrink, normalize, similarity)

    def get_itemsim_CF(self, URM, knn, shrink, normalize=True, similarity='cosine', tfidf=True):
        UCM = self.get_UCM(URM, tfidf)

        try:
            try:
                item_sim = sp.load_npz("../data/item_sim.npz")
            except FileNotFoundError:
                item_sim = sp.load_npz("app/data/item_sim.npz")
            print("similarity matrix loaded from file")
        except:
            print("similarity matrix non available, proceed to compute")
            item_sim = self.get_similarity(UCM, knn, shrink, normalize, similarity)
            sp.save_npz("../data/item_sim.npz", item_sim)
        return item_sim
