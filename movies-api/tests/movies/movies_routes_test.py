from movies_api.movies.routes import movies_bp
from flask import Flask
import pytest
from movies_api.movies.models import Movie
from movies_api.utils import db, jwt, cache
from flask_jwt_extended import create_access_token
from unittest.mock import patch
import datetime


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test"
    app.config["OMDB_API_KEY"] = "test"
    app.config["OMDB_URL"] = "http://www.example.com"
    app.config["CACHE_TYPE"] = "SimpleCache"
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    app.register_blueprint(movies_bp)
    with app.app_context():
        db.create_all()
        movie1 = Movie(
            "Movie 1",
            "id235",
            2021,
            5,
            "Action",
            "Philip Max",
            datetime.date(2021, 1, 1),
            None,
        )
        movie2 = Movie(
            "Movie 2",
            "id236",
            2022,
            6,
            "Drama",
            "Johan Sebastian Mastropiero",
            datetime.date(2022, 1, 1),
            None,
        )
        movie3 = Movie(
            "Movie 3",
            "id237",
            2023,
            7,
            "Comedy",
            "John Doe",
            datetime.date(2023, 1, 1),
            None,
        )
        db.session.add(movie1)
        db.session.add(movie2)
        db.session.add(movie3)
        db.session.commit()
        yield app
        db.drop_all()
        cache.clear()


def test_get_movies(app):
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json["movies"]) == 3
    assert response_json["movies"][0]["title"] == "Movie 1"
    assert response_json["movies"][1]["title"] == "Movie 2"
    assert response_json["movies"][0]["year"] == 2021
    assert response_json["movies"][1]["year"] == 2022
    assert response_json["movies"][0]["director"] == "Philip Max"
    assert response_json["movies"][1]["director"] == "Johan Sebastian Mastropiero"
    assert response_json["movies"][0]["genre"] == "Action"
    assert response_json["movies"][1]["genre"] == "Drama"
    assert response_json["movies"][0]["runtime"] == "5 min"
    assert response_json["movies"][1]["runtime"] == "6 min"
    assert response_json["movies"][0]["imdb_id"] == "id235"
    assert response_json["movies"][1]["imdb_id"] == "id236"
    assert response_json["movies"][2]["title"] == "Movie 3"
    assert response_json["movies"][2]["year"] == 2023
    assert response_json["movies"][2]["director"] == "John Doe"
    assert response_json["movies"][2]["genre"] == "Comedy"
    assert response_json["movies"][2]["runtime"] == "7 min"
    assert response_json["movies"][2]["imdb_id"] == "id237"
    response = client.get("/?page=1&per_page=1")
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json["movies"]) == 1
    assert response_json["movies"][0]["title"] == "Movie 1"
    response = client.get("/?page=2&per_page=1")
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json["movies"]) == 1
    assert response_json["movies"][0]["title"] == "Movie 2"
    response = client.get("/?page=3&per_page=1")
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json["movies"]) == 1
    assert response_json["movies"][0]["title"] == "Movie 3"
    with app.app_context():
        db.drop_all()
    response = client.get("/?page=3&per_page=1")
    assert response.status_code == 200
    assert response_json == response.get_json()
    cache.clear()
    response = client.get("/")
    assert response.status_code == 500
    response_json = response.get_json()
    assert response_json["error"] == "could't get the movies from the database"


def test_get_one(app):
    client = app.test_client()
    response = client.get("/get_one?title=Movie 1")
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json["title"] == "Movie 1"
    assert response_json["year"] == 2021
    assert response_json["director"] == "Philip Max"
    assert response_json["genre"] == "Action"
    assert response_json["runtime"] == "5 min"
    assert response_json["imdb_id"] == "id235"
    # Since the movie is already in the cache, if I delete it from the database without invalidating the cache, the movie will still be returned
    db.drop_all()
    response = client.get("/get_one?title=Movie 1")
    assert response.status_code == 200
    assert response_json == response.get_json()


def test_get_one_not_found(app):
    client = app.test_client()
    response = client.get("/get_one?title=Movie 4")
    assert response.status_code == 404
    response_json = response.get_json()
    assert response_json["error"] == "Movie not found"


def test_get_one_no_title(app):
    client = app.test_client()
    response = client.get("/get_one")
    assert response.status_code == 400
    response_json = response.get_json()
    assert response_json["error"] == "Title is required"


def test_get_one_db_exception(app):
    client = app.test_client()
    db.drop_all()
    response = client.get("/get_one?title=Movie 1")
    assert response.status_code == 500
    response_json = response.get_json()
    assert response_json["error"] == "could't get the movie from the database"


def test_get_by_id(app):
    client = app.test_client()
    cache.clear()
    response = client.get("/1")
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json["title"] == "Movie 1"
    assert response_json["year"] == 2021
    assert response_json["director"] == "Philip Max"
    assert response_json["genre"] == "Action"
    assert response_json["runtime"] == "5 min"
    assert response_json["imdb_id"] == "id235"
    db.drop_all()
    response = client.get("/1")
    assert response.status_code == 200
    assert response_json == response.get_json()


def test_get_by_id_not_found(app):
    client = app.test_client()
    response = client.get("/4")
    assert response.status_code == 404
    response_json = response.get_json()
    assert response_json["error"] == "Movie not found"


def test_get_by_id_db_exception(app):
    client = app.test_client()
    db.drop_all()
    response = client.get("/1")
    assert response.status_code == 500
    response_json = response.get_json()
    assert response_json["error"] == "could't get the movie from the database"


def test_add_movie(app):
    client = app.test_client()
    response = client.post("/add", json={"title": "Movie 4"})
    mock_response = {"Title": "Movie 4", "Year": "2024", "imdbID": "id238"}
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        response = client.post("/add", json={"title": "Movie 4"})
        assert response.status_code == 201
        response_json = response.get_json()
        assert response_json["title"] == "Movie 4"
        assert response_json["year"] == 2024
        assert response_json["imdb_id"] == "id238"
        movie = db.session.get(Movie, response_json["id"])
        assert movie is not None
        assert movie.title == "Movie 4"


def test_add_movie_imdbid_clash(app):
    client = app.test_client()
    response = client.post("/add", json={"title": "Movie 4"})
    mock_response = {"Title": "Movie 4", "Year": "2024", "imdbID": "id235"}
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        response = client.post("/add", json={"title": "Movie 4"})
        assert response.status_code == 500


def test_add_movie_no_title(app):
    client = app.test_client()
    response = client.post("/add", json={"non_title": "Movie 1"})
    assert response.status_code == 400
    response_json = response.get_json()
    assert response_json["error"] == "Title is required"


def test_add_movie_already_exists(app):
    client = app.test_client()
    response = client.post("/add", json={"title": "Movie 1"})
    assert response.status_code == 400
    response_json = response.get_json()
    assert response_json["error"] == "Movie already exists"


def test_add_movie_not_found(app):
    client = app.test_client()
    mock_response = None
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        response = client.post("/add", json={"title": "Movie 5"})
        assert response.status_code == 404
        response_json = response.get_json()
        assert response_json["error"] == "Movie not found"


def test_add_movie_not_found_with_response_eq_false(app):
    client = app.test_client()
    mock_response = {"Response": "False"}
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        response = client.post("/add", json={"title": "Movie 5"})
        assert response.status_code == 404
        response_json = response.get_json()
        assert response_json["error"] == "Movie not found"


def test_add_movie_parse_error(app):
    client = app.test_client()
    mock_response = {"Title": "Movie 6"}
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        response = client.post("/add", json={"title": "Movie 6"})
        assert response.status_code == 500
        response_json = response.get_json()
        assert response_json["error"] == "could't parse the external movie data"


def test_add_movie_db_exception(app):
    client = app.test_client()
    response = client.post("/add", json={"title": "Movie 7"})
    mock_response = {"Title": "Movie 7", "Year": "2027", "imdbID": "id239"}
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        db.drop_all()
        response = client.post("/add", json={"title": "Movie 7"})
        assert response.status_code == 500


def test_delete_movie(app):
    client = app.test_client()
    token = create_access_token(identity=1)
    response = client.delete("/1/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204
    assert db.session.get(Movie, 1) is None
    assert db.session.query(Movie).count() == 2


def test_delete_movie_not_found(app):
    client = app.test_client()
    token = create_access_token(identity=1)
    response = client.delete("/4/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    response_json = response.get_json()
    assert response_json["error"] == "Movie not found"


def test_delete_movie_db_exception(app):
    client = app.test_client()
    db.drop_all()
    token = create_access_token(identity=1)
    response = client.delete("/1/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 500
