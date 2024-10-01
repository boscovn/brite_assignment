from flask import Blueprint, request, current_app
from movies_api.services.omdb import get_movie_by_title
from .models import Movie
from flask_jwt_extended import jwt_required
from movies_api.utils import db, cache
from flask import current_app
import logging

logger = logging.getLogger(__name__)


movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/", methods=["GET"])
@cache.cached(timeout=60, query_string=True, key_prefix="movies")
def get_movies():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    try:
        movies = (
            db.session.query(Movie).limit(per_page).offset((page - 1) * per_page).all()
        )
        current_app.logger.info(f"Found {len(movies)} movies in the database")
        return {"movies": [movie.to_dict() for movie in movies]}
    except Exception as e:
        logger.error(f"Error getting movies from the database: {e}")
        return {"error": "could't get the movies from the database"}, 500


@movies_bp.route("/get_one", methods=["GET"])
@cache.cached(timeout=60, query_string=True, key_prefix="movie_by_title")
def get_one():
    title = request.args.get("title")
    if title is None:
        return {"error": "Title is required"}, 400
    try:
        movie = db.session.query(Movie).filter_by(title=title).first()
        if movie is None:
            return {"error": "Movie not found"}, 404
        return movie.to_dict(), 200
    except Exception as e:
        logger.error(f"Error getting movie from the database: {e}")
        return {"error": "could't get the movie from the database"}, 500


@movies_bp.route("/<int:id>", methods=["GET"])
@cache.cached(timeout=60, query_string=True, key_prefix="movie_by_id")
def get_movie(id):
    try:
        movie = db.session.query(Movie).filter_by(id=id).first()
        if movie is None:
            return {"error": "Movie not found"}, 404
        return movie.to_dict(), 200
    except Exception as e:
        logger.error(f"Error getting movie from the database: {e}")
        return {"error": "could't get the movie from the database"}, 500


@movies_bp.route("/add", methods=["POST"])
def add_movie():
    data = request.get_json()
    title = data.get("title")
    if title is None:
        return {"error": "Title is required"}, 400
    existing_movie = db.session.query(Movie).filter_by(title=title).count()
    if existing_movie > 0:
        return {"error": "Movie already exists"}, 400
    try:
        response = get_movie_by_title(
            current_app.config["OMDB_API_KEY"],
            current_app.config["OMDB_URL"],
            title,
        )
    except Exception as e:
        logger.error(f"Error getting movie data from external API: {e}")
        return {"error": "could't get the movie data from the external API"}, 501
    if response is None:
        return {"error": "Movie not found"}, 404
    if response.get("Response") == "False":
        return {"error": "Movie not found"}, 404
    try:
        movie = Movie.from_open_movie_db(response)
    except ValueError as e:
        logger.error(f"Error parsing external movie data: {e}, {response}")
        return {"error": "could't parse the external movie data"}, 500
    try:
        db.session.add(movie)
        db.session.commit()
        cache.delete_memoized(get_movies)
        cache.delete_memoized(get_one)
        return movie.to_dict(), 201
    except Exception as e:
        logger.error(f"Error adding movie to the database: {e}")
        return {"error": "could't add the movie to the database"}, 500


@movies_bp.route("/<int:id>/delete", methods=["DELETE"])
@jwt_required()
def delete_movie(id):
    try:
        res = db.session.query(Movie).filter_by(id=id).delete()
        db.session.commit()
        logger.info(f"Deleted movie from the database with id {id}")
        if res == 0:
            return {"error": "Movie not found"}, 404
        cache.delete_memoized(get_movie, id=id)
        cache.delete_memoized(get_one)
        cache.delete_memoized(get_movies)
        return "", 204
    except Exception as e:
        logger.error(f"Error deleting movie from the database: {e}")
        return {"error": "could't delete the movie from the database"}, 500
