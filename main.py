from classifiers.decision_tree import tree_classify
from classifiers.evaluations_classifier import classify_users
from classifiers.random_forest import forest_classify
from features_extractor import fetch_movie_data, count_movies_distance
from knn_algorithm import knn_classify, knn_classify_users
from normalizer import normalize_column
from read_csv import read_csv, read_csv1
import numpy as np
import pandas as pd
import params as p

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


    if p.object_type == 'users':
        print("Started user classification")
        for test_user_id in test_evaluations.keys():
            for test_eval in test_evaluations[test_user_id]:
                ranking = {}
                for train_user_id in train_evaluations.keys():
                    if test_eval.movie_id in ([obj.movie_id for obj in train_evaluations[train_user_id]]):
                        ranking[train_user_id] = classify_users(train_evaluations[train_user_id], train_evaluations[test_user_id])
                print("Test user id")
                print(test_user_id)
                test_label = knn_classify_users(5, test_eval.movie_id, train_evaluations, ranking)
                test_eval.evaluation = test_label
                print(test_label)
        print("Finished user classification")
    else:
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

                if p.method == 'kNN':
                    test_label = knn_classify(5, train_evaluations[user_id], ranking)
                elif p.method == 'decision_tree':
                    test_label = tree_classify(ranking.values, np.array(evals), last_element.values)
                elif p.method == 'random_forest':
                    test_label = forest_classify(ranking.values, np.array(evals), last_element.values)

                test_eval.evaluation = test_label

    flattened_values = [item for sublist in test_evaluations.values() for item in sublist]
    flattened_list = [(m.eval_id, m.user_id, m.movie_id, m.evaluation) for m in flattened_values]
    write_dict(p.setup["output_path"], flattened_list)

main()



