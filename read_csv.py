import csv

from movie_evaluation import MovieEvaluation


def read_csv():
    with open('movie/movie.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        movies_list = []
        for row in spamreader:
            movies_list.append(row[1])
        return movies_list


def read_csv1(is_train):
    if is_train:
        filename = 'train.csv'
    else:
        filename = 'task.csv'

    with open('movie/' + filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        dict = {}
        for row in spamreader:
            movie_evaluation = MovieEvaluation(movie_id=row[2], evaluation=row[3])
            if row[1] not in dict.keys():
                dict[row[1]] = []
            dict[row[1]].append(movie_evaluation)

        return dict

