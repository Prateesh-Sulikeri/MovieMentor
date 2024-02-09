from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests

app = Flask(__name__)

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0760666b31e986f26b94427be69b3724&language=en-US'.format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_movie_name = request.form['selected_movie']
        names, posters = recommend(selected_movie_name)
        return render_template('index.html', names=names, posters=posters, movies=movies)
    return render_template('index.html', names=None, posters=None, movies=movies)



