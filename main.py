from classifiers.decision_tree import classify
from controller import get_movie_actors, get_movie_details, get_movie_keywords
from features_extractor import fetch_movie_data, count_movies_distance
from knn_algorithm import knn_classify
from normalizer import normalize_column
from read_csv import read_csv, read_csv1
import numpy as np
import pandas as pd

from write_csv import write_dict


def main():
    movies = read_csv()
    train_evaluations = read_csv1(is_train=True)
    test_evaluations = read_csv1(is_train=False)

    movies_list = {}
    print("Fetch movies")
    for index, row in movies.iterrows():
        movies_list.update(fetch_movie_data(row["tmdb_id"]))
    print('Finish movies download')
    iter = 15
    for user_id in train_evaluations.keys():
        for test_eval in test_evaluations[user_id]:
            print('TaskId:')
            print(test_eval.eval_id)
            ranking = pd.DataFrame()
            test_id = movies.loc[movies['id'] == test_eval.movie_id].iloc[0]['tmdb_id']
            test_movie_score = count_movies_distance(movies_list[test_id], movies_list[test_id])
            for train_eval in train_evaluations[user_id]:
                train_id = movies.loc[movies['id'] == train_eval.movie_id].iloc[0]['tmdb_id']
                movie_score = count_movies_distance(movies_list[test_id], movies_list[train_id])
                ranking = ranking.append(movie_score, ignore_index=True)

            ranking = ranking.append(test_movie_score, ignore_index=True)
            for column_name, column_data in ranking.iteritems():
                ranking[column_name] = normalize_column(column_data)

            last_element = ranking.iloc[-1]
            ranking = ranking.sub(last_element)
            ranking = ranking.drop(ranking.index[-1])

            evals = []
            for x in train_evaluations[user_id]:
                evals += x.evaluation

            test_label = knn_classify(5, train_evaluations[user_id], ranking)
            # test_label = classify(ranking.values, np.array(evals), last_element.values)
            test_eval.evaluation = test_label
            iter = iter + 1
    flattened_values = [item for sublist in test_evaluations.values() for item in sublist]
    flattened_list = [(m.eval_id, m.user_id, m.movie_id, m.evaluation) for m in flattened_values]
    write_dict("output/knn.csv", flattened_list)

    # Flatten lists in dictionary values
    # flattened_values = [item for sublist in test_evaluations.values() for item in sublist]
    # flattened_list = [(m.id, m.user_id, m.movie_id, m.evaluation) for m in flattened_values]
    # write_dict("tree.csv", flattened_list)
main()



