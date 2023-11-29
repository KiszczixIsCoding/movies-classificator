from controller import get_movie_actors, get_movie_details, get_movie_keywords
from features_extractor import fetch_movie_data, count_movies_distance
from knn_algorithm import knn_classify
from normalizer import normalize_column
from read_csv import read_csv, read_csv1
import numpy as np
import pandas as pd

def main():
    movies = read_csv()
    train_evaluations = read_csv1(is_train=True)
    test_evaluations = read_csv1(is_train=False)

    movies_list = {}
    for index, row in movies.iterrows():
        movies_list.update(fetch_movie_data(row["tmdb_id"]))

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

            print(ranking)
            last_element = ranking.iloc[-1]
            ranking = ranking.sub(last_element)
            ranking = ranking.drop(ranking.index[-1])

            # for movie_ft_vector in ranking.iterrows():
            #     X_train = movie_ft_vector.toList()

            print(knn_classify(5, train_evaluations[user_id], ranking))
main()



