import requests

base_url = "https://api.themoviedb.org"
api_key = "?api_key=dd99229ad94125af4ce08233a6662aba"


def get_movie_details(movie_id):
    # api_url = base_url + api_key
    api_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + api_key
    response = requests.get(api_url)
    print(response.json())
    print((response.json()['relesed_date'][0]))

def get_movie_keywords(movie_id):
    # api_url = base_url + api_key
    api_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/keywords" + api_key
    response = requests.get(api_url)
    print(response.json())
    print((response.json()['keywords'][0]))


def get_movie_actors(movie_id):
    # api_url = base_url + api_key
    api_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/credits" + api_key
    response = requests.get(api_url)
    res = {key: response.json()[key] for key in response.json().keys()
           & {'id', 'cast'}}
    print(res)
    print((response.json()['cast'][0]))
    print((response.json()['crew'][0]))