from collections import Counter

def xlknn_classify(n_neighbours, user_evaluations, ranking):
    indexes = ranking.sum(axis=1).sort_values(ascending=False).index[0:n_neighbours]
    sorted_array = user_evaluations[indexes]
    evals = []
    for x in sorted_array:
        evals += x.evaluation
    counter = Counter(evals)
    most_common_element = counter.most_common(1)[0][0]

    return most_common_element

def knn_classify_users(n_neighbours, movie_id, user_evaluations, ranking):
    sorted_keys = sorted(ranking, key=lambda key: ranking[key], reverse=True)[0:n_neighbours]
    evals = []
    for key in sorted_keys:
        user_eval = next((obj for obj in user_evaluations[key] if obj.movie_id == movie_id), None)
        evals += user_eval.evaluation

    print(len(evals))
    print(evals)
    counter = Counter(evals)
    print(len(counter.most_common(1)))
    print(len(counter.most_common(1)[0]))
    most_common_element = counter.most_common(1)[0][0]

    return most_common_element