from flask import Flask, request
import json
import os

app = Flask(__name__)
# I want movies by imdbID to be populated with a json file in the same as the app.py file
# I may be running the app from a different directory so I need to use the absolute path
base_path = os.path.dirname(os.path.abspath(__file__))
movies_by_imdbID = {}
with open(f"{base_path}/movies_by_imdbID.json", "r") as f:
    movies_by_imdbID = json.load(f)

movies_by_title = {}
with open(f"{base_path}/movies_by_title.json", "r") as f:
    movies_by_title = json.load(f)


@app.route("/")
def get_movie_by_title():
    title = request.args.get("t")
    if title is not None:
        return movies_by_title.get(title, {}), 200
    imdbID = request.args.get("i")
    if imdbID is not None:
        return movies_by_imdbID.get(imdbID, {}), 200
    page = request.args.get("page")
    if page is not None:
        page = int(page)
        if page is None or page < 1:
            return "Page not found", 404
        page_size = 10
        start = (page - 1) * page_size
        end = start + page_size
        movies = list(movies_by_imdbID.keys())
        if start >= len(movies):
            return "Page not found", 404
        movies = movies[start:end]
        movies = [{"imdbID": imdbID} for imdbID in movies]
        return {"Search": movies}, 200

    return "Movie not found", 404


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run()
