def classify_users(test_evaluations, train_evaluations):
    ids = [obj.movie_id for obj in train_evaluations]
    ids1 = [obj.movie_id for obj in test_evaluations]
    common_ids = [movie_id for movie_id in ids if movie_id in ids1]

    print(common_ids)

    same_evals_counter = 0
    for id in common_ids:
        train_movie = next((obj for obj in train_evaluations if obj.movie_id == id), None)
        test_movie = next((obj for obj in test_evaluations if obj.movie_id == id), None)

        if train_movie.evaluation == test_movie.evaluation:
            same_evals_counter = same_evals_counter + 1

    return same_evals_counter / len(common_ids)


