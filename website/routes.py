from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Movie
from . import db
from config import config

import json
import requests

routes = Blueprint('routes', __name__)

API_KEY = config["movie_db_api_key"]
MOVIE_DB_URL = "https://api.themoviedb.org/3/"

# Endpoint for homepage.
@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():

    # The POST request takes the value of the input and uses it to query the movie API.
    if request.method == 'POST':
        search = json.loads(request.data)
        sstring = search["search"]
        url = f"{MOVIE_DB_URL}search/movie?api_key={API_KEY}&query={sstring}"
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    # If it's a GET request, return the page to the user.
    return render_template("home.html", user=current_user)

# Endpoint for Movie page and handling the ratings.
@routes.route('/movie', methods=['GET', 'POST'])
@login_required
def movie():
    # The movie id is parced and passed through the URL as a param: id.
    id = request.args.get('id', None)
    url = f"{MOVIE_DB_URL}movie/{id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = json.loads(response.text)
    movie = Movie.query.get(id)

    # POST requests are used to rate the movie.
    if request.method == 'POST':
        rating = request.form.get('rating')
        butter = request.form.get('butter')
        name = request.form.get('name')
        poster = request.form.get('poster')
        # If no poster exits we use a fallback image.
        if(not poster):
            poster = "https://picsum.photos/200/300"
        # If there is a movie we update the ratings, otherwise we create a new entry into the database.
        if (movie):
            movie.rating = rating
            movie.butter = butter
            movie.name = name
            movie.poster = poster
            db.session.commit()
        else:
            new_movie = Movie(butter=butter, rating=rating, id=current_user.id, name=name, poster=poster)
            db.session.add(new_movie)
            db.session.commit()
        return redirect(url_for('routes.home'))
    # If it's a GET request return the movie page with the movie data.
    return render_template("movie.html", user=current_user, data=data,movie=movie)

# Remove endpoint is used to delete an entry from the database.
# Only handles POST requests.
@routes.route('/remove', methods=['POST'])
@login_required
def remove():
    id = request.args.get('id', None)
    movie = Movie.query.get(id)
    if movie:
        if movie.id == current_user.id:
            db.session.delete(movie)
            db.session.commit()
            return redirect(url_for('routes.home'))