import csv

from movie_evaluation import MovieEvaluation


def read_csv():
    with open('movie/movie.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            print(', '.join(row))

def read_csv1():
    with open('movie/train.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')

        dict = {}
        for row in spamreader:
            movie_evaluation = MovieEvaluation(movie_id=row[2], evaluation=row[3])
            if row[1] not in dict.keys():
                dict[row[1]] = []
            dict[row[1]].append(movie_evaluation)

        print(len(dict['1642']))

