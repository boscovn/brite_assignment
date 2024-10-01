from flask import Flask, request

app = Flask(__name__)
movies = {
    "Forrest Gump": {"imdb": 8.8, "year": 1994},
    "3 Idiots": {"imdb": 8.4, "year": 2009},
    "The Dark Knight": {"imdb": 9.0, "year": 2008},
}


@app.route("/")
def get_movie_by_title():
    title = request.args.get("t")
    if title is None:
        return "no title", 400
    return movies.get(title, {}), 200


@app.route("/health")
def health():
    return "OK", 200
