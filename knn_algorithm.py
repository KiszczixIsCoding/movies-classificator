from collections import Counter

def knn_classify(n_neighbours, movies_array):
    sorted_array = sorted(movies_array, key=lambda x: x[1])
    counter = Counter(sorted_array[0:n_neighbours])
    most_common_element = counter.most_common(1)[0][0]
    return most_common_element