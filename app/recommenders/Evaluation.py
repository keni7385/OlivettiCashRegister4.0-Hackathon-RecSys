import pandas as pd
import numpy as np
import scipy.sparse as sp


class Eval(object):

    def __init__(self, u):
        self.URM = u.URM
        self.train_sequential = u.train_sequential
        self.target_playlists = u.target_playlists
        self.URM_test = None
        self.test_playlists = None

    def generate_predictions(self, recommender, path, target_receipt):
        target_playlists = self.target_playlists
        final_result = pd.DataFrame(index=range(target_playlists.shape[0]), columns=('playlist_id', 'track_ids'))

        for i, user_id in tqdm(enumerate(np.array(target_playlists))):
            recommended_items = recommender.recommend(int(user_id))

            if len(recommended_items) != 10:
                print(len(recommended_items))

            final_result['playlist_id'][i] = int(user_id)
            string_rec = ' '.join(map(str, recommended_items.reshape(1, 10)[0]))
            final_result['track_ids'][i] = string_rec

        final_result.to_csv(path, index=False)
