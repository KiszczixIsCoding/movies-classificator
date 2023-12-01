class MovieEvaluation:
    def __init__(self, eval_id, user_id,  movie_id, evaluation):
        self.eval_id = eval_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.evaluation = evaluation

    def to_dict(self):
        return {
            'id': self.eval_id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'evaluation': self.evaluation
        }