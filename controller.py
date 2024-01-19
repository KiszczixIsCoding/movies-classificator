import requests

from datetime import datetime

base_url = "https://api.themoviedb.org"
api_key = "?api_key=dd99229ad94125af4ce08233a6662aba"

def get_movie_details(movie_id):
    # api_url = base_url + api_key
    api_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + api_key
    response = requests.get(api_url)
    id = response.json()['id']
    release_date_obj = datetime.strptime(response.json()['release_date'], '%Y-%m-%d')
    budget = response.json()['budget']
    runtime = response.json()['runtime']
    overview = response.json()['overview']
    vote_average = response.json()['vote_average']
    revenue = response.json()['revenue']

    genre_ids = [entry["id"] for entry in response.json()['genres']]
    return {
        'id': id,
        'release_date': release_date_obj.year,
        'budget': budget,
        'genre_ids': genre_ids,
        'runtime': runtime,
        'overview': overview,
        'vote_average': vote_average,
        'revenue': revenue
    }

def get_movie_keywords(movie_id):
    api_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/keywords" + api_key
    response = requests.get(api_url)
    keyword_ids = [entry["id"] for entry in response.json()['keywords']]
    return {
        'keyword_ids': keyword_ids
    }


def get_movie_actors(movie_id):
    # api_url = base_url + api_key
    api_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/credits" + api_key
    response = requests.get(api_url)
    res = {key: response.json()[key] for key in response.json().keys()
           & {'id', 'cast'}}

    cast_ids = [entry["id"] for entry in response.json()['cast'][0:10]]
    crew_ids = [entry["id"] for entry in response.json()['crew'][0:3]]
    return {'cast_ids': cast_ids, 'crew_ids': crew_ids}