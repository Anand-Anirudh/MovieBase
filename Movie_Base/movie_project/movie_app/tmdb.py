import requests
api_key="a0e658d14540c501d60bf848cbab3db0"
def search_movies(query, api_key):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={query}"
    response = requests.get(url)
    movie_data = response.json()
    return movie_data['results']



