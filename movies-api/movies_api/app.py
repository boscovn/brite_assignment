from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
import movies_api.config as config
from movies_api.utils import db, jwt, cache
from dotenv import load_dotenv
from movies_api.movies.models import Movie
from movies_api.movies.routes import movies_bp
from movies_api.users.models import User
from movies_api.users.routes import users_bp
import asyncio
import os
from movies_api.movies.models import Movie
from movies_api.services.omdb import get_n_movies


async def populate_db(n: int, url: str, api_key: str, app_db: SQLAlchemy):
    for movie in await get_n_movies(api_key, url, n):
        try:
            app_db.session.add(Movie.from_open_movie_db(movie))

        except Exception as e:
            print("Error adding movie to db: ", e)
    app_db.session.commit()


app = Flask(__name__)
config_name = os.environ.get("FLASK_ENV", "Development")
if config_name == "Production":
    app.config.from_object(config.ProductionConfig)
elif config_name == "Testing":
    app.config.from_object(config.TestingConfig)
elif config_name == "Development":
    load_dotenv()
    app.config.from_object(config.DevelopmentConfig)
else:
    print("Invalid FLASK_ENV value")
    exit(1)

db.init_app(app)
jwt.init_app(app)
cache.init_app(app)
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(movies_bp, url_prefix="/movies")
if config_name != "Testing":
    with app.app_context():
        db.create_all()
        if Movie.query.count() == 0:
            asyncio.run(
                populate_db(
                    100,
                    app.config["OMDB_URL"],
                    app.config["OMDB_API_KEY"],
                    db,
                )
            )
        if User.query.count() == 0:
            user = User(
                username=app.config["DEFAULT_USER"],
                password=app.config["DEFAULT_PASSWORD"],
            )
            db.session.add(user)
            db.session.commit()


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    app.logger.warning(e)
    return {"message:": f"{e.description}"}, e.code


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(e)
    return {"message:": "An error occurred"}, 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
