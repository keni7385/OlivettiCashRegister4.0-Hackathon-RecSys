class Eval(object):

    def __init__(self, u):
        self.URM = u.URM
        self.URM_test = None

    def generate_predictions(self, recommender, path, target_receipt):

        recommended_items = recommender.recommend(target_receipt)

        if len(recommended_items) != 3:
            print(len(recommended_items))

        # return list of recommended items
        return recommended_items
