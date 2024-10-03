from movies_api.movies.models import Movie
import datetime
from movies_api.utils import db
from flask import Flask
import pytest


@pytest.fixture
def setup():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield
        db.drop_all()


def test_movie(setup):
    movies = Movie.query.all()
    assert len(movies) == 0
    movie = Movie(
        title="Test Movie",
        year=2021,
        imdb_id="tt1234567",
        genre="Action",
        director="John Doe",
        runtime=120,
        poster="https://www.example.com/poster.jpg",
        release_date=datetime.date(2021, 1, 1),
    )
    db.session.add(movie)
    db.session.commit()
    movies = Movie.query.all()
    assert len(movies) == 1
    assert movies[0].id == 1
    assert movies[0].title == "Test Movie"
    assert movies[0].year == 2021
    assert movies[0].imdb_id == "tt1234567"
    assert movies[0].genre == "Action"
    assert movies[0].director == "John Doe"
    assert movies[0].runtime == 120
    assert movies[0].poster == "https://www.example.com/poster.jpg"
    assert movies[0].release_date == datetime.date(2021, 1, 1)


def test_movie_to_dict():
    movie = Movie(
        title="Test Movie",
        year=2021,
        imdb_id="tt1234567",
        genre="Action",
        director="John Doe",
        runtime=120,
        poster="https://www.example.com/poster.jpg",
        release_date=datetime.date(2021, 1, 1),
    )
    movie_dict = movie.to_dict()
    assert movie_dict["id"] == None
    assert movie_dict["title"] == "Test Movie"
    assert movie_dict["year"] == 2021
    assert movie_dict["imdb_id"] == "tt1234567"
    assert movie_dict["genre"] == "Action"
    assert movie_dict["director"] == "John Doe"
    assert movie_dict["runtime"] == "120 min"
    assert movie_dict["poster"] == "https://www.example.com/poster.jpg"
    assert movie_dict["release_date"] == "01/01/2021"


def test_from_open_movie_db(setup):
    data = {
        "Title": "Test Movie",
        "Year": "2021",
        "imdbID": "tt1234567",
        "Runtime": "120 min",
        "Response": "True",
        "Genre": "Action",
        "Director": "John Doe",
        "Poster": "https://www.example.com/poster.jpg",
        "Released": "01 Jan 2021",
    }
    movie = Movie.from_open_movie_db(data)
    assert movie.title == "Test Movie"
    assert movie.year == 2021
    assert movie.imdb_id == "tt1234567"
    assert movie.runtime == 120
    assert movie.genre == "Action"
    assert movie.director == "John Doe"
    assert movie.poster == "https://www.example.com/poster.jpg"
    assert movie.release_date == datetime.date(2021, 1, 1)


def test_from_open_movie_db_invalid_title():
    data = {
        "Title": 123,
        "Year": "2021",
        "imdbID": "tt1234567",
        "Runtime": "120 min",
        "Response": "True",
        "Genre": "Action",
        "Director": "John Doe",
        "Poster": "https://www.example.com/poster.jpg",
        "Released": "01 Jan 2021",
    }
    with pytest.raises(ValueError) as e:
        Movie.from_open_movie_db(data)


def test_from_open_movie_db_no_title():
    data = {
        "Year": "2021",
        "imdbID": "tt1234567",
        "Runtime": "120 min",
        "Response": "True",
        "Genre": "Action",
        "Director": "John Doe",
        "Poster": "https://www.example.com/poster.jpg",
        "Released": "01 Jan 2021",
    }
    with pytest.raises(ValueError) as e:
        Movie.from_open_movie_db(data)


def test_from_open_movie_db_no_imdb_id():
    data = {
        "Title": "Test Movie",
        "Year": "2021",
        "Runtime": "120 min",
        "Response": "True",
        "Genre": "Action",
        "Director": "John Doe",
        "Poster": "https://www.example.com/poster.jpg",
        "Released": "01 Jan 2021",
    }
    with pytest.raises(ValueError) as e:
        Movie.from_open_movie_db(data)


def test_from_open_movie_response_false():
    data = {
        "Response": "False",
    }
    with pytest.raises(ValueError) as e:
        Movie.from_open_movie_db(data)


def test_from_open_movie_db_invalid_year():
    data = {
        "Title": "Test Movie",
        "Year": False,
        "imdbID": "tt1234567",
        "Runtime": "120 min",
        "Response": "True",
        "Genre": "Action",
        "Director": "John Doe",
        "Poster": "https://www.example.com/poster.jpg",
        "Released": "01 Jan 2021",
    }
    movie = Movie.from_open_movie_db(data)
    assert movie.year == None


def test_from_open_movie_db_invalid_runtime(setup):
    data = {
        "Title": "Test Movie",
        "Year": "2021",
        "imdbID": "tt1234567",
        "Runtime": "seven minutes",
        "Response": "True",
        "Genre": "Action",
        "Director": "John Doe",
        "Poster": "https://www.example.com/poster.jpg",
        "Released": "01 Jan 2021",
    }
    movie = Movie.from_open_movie_db(data)
    assert movie.runtime == None


def test_from_open_movie_db_invalid_release_date(setup):
    data = {
        "Title": "Test Movie",
        "Year": "2021",
        "imdbID": "tt1234567",
        "Runtime": "120 min",
        "Response": "True",
        "Genre": "Action",
        "Director": "John Doe",
        "Poster": "https://www.example.com/poster.jpg",
        "Released": "01/01/2021",
    }
    movie = Movie.from_open_movie_db(data)
    assert movie.release_date == None
