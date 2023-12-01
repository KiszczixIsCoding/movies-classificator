import csv

from movie_evaluation import MovieEvaluation
import pandas as pd
import numpy as np

def read_csv():
    with open('movie/movie.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        movies_list = []
        for row in spamreader:
            movies_list.append({'id': row[0], "tmdb_id": row[1]})

        df = pd.DataFrame(movies_list)
        return df


def read_csv1(is_train):
    if is_train:
        filename = 'train.csv'
    else:
        filename = 'task.csv'

    with open('movie/' + filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        dict = {}
        for row in spamreader:
            movie_evaluation = MovieEvaluation(eval_id=row[0], user_id=row[1], movie_id=row[2], evaluation=row[3])
            if row[1] not in dict.keys():
                dict[row[1]] = np.array([])
            dict[row[1]] = np.concatenate((dict[row[1]], np.array([movie_evaluation])))

        return dict

