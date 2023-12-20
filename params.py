method = 'kNN'
object_type = 'users'

kNN_movies_setup = {
    'n_neighbours': 5
}

decision_tree_movies_setup = {
    'output_path': "output/submission_tree.csv"
}

random_forest_movies_setup = {
    'output_path': "output/submission_forest.csv"
}

kNN_users_setup = {
    'n_neighbours': 5,
    'output_path': "output/submission.csv"
}
if object_type == 'users':
    setup = kNN_users_setup
else:
    if method == 'kNN':
        setup = kNN_movies_setup
    elif method == 'decision_tree':
        setup = decision_tree_movies_setup
    elif method == 'random_forest':
        setup = random_forest_movies_setup
