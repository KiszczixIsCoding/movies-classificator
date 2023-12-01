from controller import get_movie_keywords, get_movie_actors, get_movie_details
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def merge_util(arr1, arr2):
    np_arr1 = np.array(arr1)
    np_arr2 = np.array(arr2)

    return len(np.intersect1d(np_arr1, np_arr2)) / len(np_arr1)

def count_text_distance(text1, text2):
    texts = [text1, text2]
    vectorizer = CountVectorizer()
    vectorized_texts = vectorizer.fit_transform(texts)
    cosine_sim = cosine_similarity(vectorized_texts)[0][0]
    return cosine_sim

def fetch_movie_data(movie_id):
    dic1 = get_movie_keywords(movie_id)
    dic2 = get_movie_actors(movie_id)
    dic3 = get_movie_details(movie_id)
    print(movie_id)
    dic = {**dic1, **dic2, **dic3}
    return {movie_id: dic}


def count_movies_distance(test_movie, train_movie):
    release_date_ft = train_movie['release_date']
    budget_ft = train_movie['budget']
    vote_average_ft = train_movie['vote_average']
    overview_ft = count_text_distance(test_movie['overview'], train_movie['overview'])
    keyword_ft = merge_util(test_movie['keyword_ids'], train_movie['keyword_ids'])
    genre_ft = merge_util(test_movie['genre_ids'], train_movie['genre_ids'])
    cast_ft = merge_util(test_movie['cast_ids'], train_movie['cast_ids'])
    crew_ft = merge_util(test_movie['crew_ids'], train_movie['crew_ids'])

    return {
        'release_date': release_date_ft,
        'budget': budget_ft,
        'vote_average_ft': vote_average_ft,
        'overview': overview_ft,
        'keyword': keyword_ft,
        'genre': genre_ft,
        'cast': cast_ft,
        'crew': crew_ft,
    }
    # return (release_date_ft + budget_ft + keyword_ft + genre_ft + cast_ft + crew_ft) / 6
