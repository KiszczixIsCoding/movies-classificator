from controller import get_movie_actors, get_movie_details, get_movie_keywords
from features_extractor import fetch_movie_data, count_movies_distance
from read_csv import read_csv, read_csv1
import numpy as np
import pandas as pd

def main():
    movies = read_csv()
    train_evaluations = read_csv1(is_train=True)
    test_evaluations = read_csv1(is_train=False)

    movies_list = {}
    for x in movies:
        movies_list.update(fetch_movie_data(x))

    for user_id in train_evaluations.keys():
        all_evaluations = train_evaluations[user_id]
        all_evaluations.extend(test_evaluations[user_id])
        for test_eval in test_evaluations[user_id]:
            arr = []
            for train_eval in train_evaluations[user_id]:
                print(test_eval.movie_id)
                print(train_eval.movie_id)
                score = count_movies_distance(movies_list[test_eval.movie_id], movies_list[train_eval.movie_id])
                arr = arr.append([train_eval, score])
            # test_label = knn_classify()
    # max_budget = max(movies_list.values(), key=lambda x: x['budget'])['budget']
    # max_runtime = max(movies_list.values(), key=lambda x: x['runtime'])['runtime']
main()



