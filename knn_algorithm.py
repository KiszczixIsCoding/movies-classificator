from collections import Counter

def knn_classify(n_neighbours, user_evaluations, ranking):
    indexes = ranking.sum(axis=1).sort_values(ascending=False).index[0:n_neighbours]
    sorted_array = user_evaluations[indexes]
    evals = []
    for x in sorted_array:
        evals += x.evaluation
        print(x.evaluation)
        print(x.movie_id)
    counter = Counter(sorted_array[0:n_neighbours])
    most_common_element = counter.most_common(1)[0][0]
    return most_common_element