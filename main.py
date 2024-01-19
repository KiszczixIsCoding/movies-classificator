import random

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix

from classifiers.decision_tree import tree_classify
from classifiers.evaluations_classifier import classify_users
from classifiers.random_forest import forest_classify
from features_extractor import fetch_movie_data, count_movies_distance
from knn_algorithm import knn_classify, knn_classify_users
from metrics_counter import count_confusion_matrix
from normalizer import normalize_column
from read_csv import read_csv, read_csv1
import numpy as np
import pandas as pd
import params as p
import classifiers.algorithms as alg
import copy

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

    validation_evaluations = {}
    if p.test:
        test_evaluations_results = {}
        val_evaluations = {}
        for index, item in train_evaluations.items():
            test_evaluations_results[index] = copy.deepcopy(item[60:90])
            val_evaluations[index] = copy.deepcopy(item[60:90])
            for item_eval in test_evaluations_results[index]:
                item_eval.evaluation = None
            train_evaluations[index] = copy.deepcopy(item[0:60])

        validation_evaluations = val_evaluations
        test_evaluations = test_evaluations_results

    if p.object_type == 'users':
        print("Started user classification")

        for test_user_id in test_evaluations.keys():
            for test_eval in test_evaluations[test_user_id]:
                ranking = {}
                for train_user_id in train_evaluations.keys():
                    if test_eval.movie_id in ([obj.movie_id for obj in train_evaluations[train_user_id]]):
                        ranking[train_user_id] = classify_users(train_evaluations[train_user_id],
                                                                train_evaluations[test_user_id])

                if ranking:
                    test_label = knn_classify_users(5, test_eval.movie_id, train_evaluations, ranking)
                    test_eval.evaluation = test_label
                else:
                    test_eval.evaluation = random.randint(0, 5)

        print("Finished user classification")
        list1_val = []
        list2_test = []
        for test_user_id in validation_evaluations.keys():
            for test_eval in validation_evaluations[test_user_id]:
                list1_val.append(int(test_eval.evaluation))
        for test_user_id in test_evaluations.keys():
            for test_eval in test_evaluations[test_user_id]:
                list2_test.append(int(test_eval.evaluation))

        count_confusion_matrix(list1_val, list2_test)

    elif p.object_type == 'movies':
        for user_id in train_evaluations.keys():
            for test_eval in test_evaluations[user_id]:
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

    else:
        collab_users_ft = {}
        collab_movies_ft = {}
        n = 10
        for i in range(0, 10):
            for user_id in train_evaluations.keys():
                if user_id not in collab_users_ft.keys() or collab_users_ft[user_id].size == 0:
                    parameters = np.random.uniform(low=-1, high=1, size=n + 1)
                    collab_users_ft[user_id] = parameters

            for index, movie in movies.iterrows():
                if movie["id"] not in collab_movies_ft.keys() or collab_movies_ft[movie["id"]].size == 0:
                    features = np.random.uniform(low=-1, high=1, size=n)
                    collab_movies_ft[movie["id"]] = features

            print("Get to train evaluations")
            for user_id in train_evaluations.keys():
                d_parameters = np.zeros(n + 1, dtype=np.longdouble)
                for index in range(len(d_parameters)):
                    sum = 0
                    for eval in train_evaluations[user_id]:
                        if index == 0:
                            sum += (alg.count_collab_parameter(collab_users_ft[user_id], collab_movies_ft[eval.movie_id]) - float(eval.evaluation))
                        else:
                            sum += ((alg.count_collab_parameter(collab_users_ft[user_id], collab_movies_ft[eval.movie_id]) - float(eval.evaluation)) * collab_movies_ft[eval.movie_id][index - 1])

                    d_parameters[index] = sum * 0.001
                    collab_users_ft[user_id] = collab_users_ft[user_id] - d_parameters
                    # print(collab_users_ft[user_id])
            print("Exit train evaluations")

            for index, movie in movies.iterrows():

                movie_id = movie.id
                keys_with_target_movie_id = [key for key, obj_list in train_evaluations.items() if
                                             any(obj.movie_id == movie_id for obj in obj_list)]
                d_features = np.zeros(n, dtype=np.longdouble)
                for index in range(len(d_features)):
                    sum = 0
                    for train_user_id in keys_with_target_movie_id:
                        user_eval = next((obj for obj in train_evaluations[train_user_id] if obj.movie_id == movie_id),
                                         None)
                        sum += ((alg.count_collab_parameter(collab_users_ft[train_user_id], collab_movies_ft[movie_id]) -
                                 float(user_eval.evaluation)) * collab_users_ft[train_user_id][index + 1])
                    d_features[index] = 0.001 * sum
                collab_movies_ft[movie_id] = collab_movies_ft[movie_id] - d_features
                print(collab_movies_ft[movie_id])

        for test_user_id in test_evaluations.keys():
            for test_eval in test_evaluations[test_user_id]:
                print(alg.count_collab_parameter(collab_users_ft[test_eval.user_id], collab_movies_ft[test_eval.movie_id]))
                evaluation = round(abs(alg.count_collab_parameter(collab_users_ft[test_eval.user_id], collab_movies_ft[test_eval.movie_id])))
                if evaluation > 5:
                    evaluation = 5
                test_eval.evaluation = evaluation

    list1_val = []
    list2_test = []
    for test_user_id in validation_evaluations.keys():
        for test_eval in validation_evaluations[test_user_id]:
            list1_val.append(int(test_eval.evaluation))
    for test_user_id in test_evaluations.keys():
        for test_eval in test_evaluations[test_user_id]:
            list2_test.append(int(test_eval.evaluation))

    count_confusion_matrix(list1_val, list2_test)
    if p.output:
        flattened_values = [item for sublist in test_evaluations.values() for item in sublist]
        flattened_list = [(m.eval_id, m.user_id, m.movie_id, m.evaluation) for m in flattened_values]
        write_dict(p.setup["output_path"], flattened_list)

main()
