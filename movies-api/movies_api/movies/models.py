from movies_api.utils import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    imdb_id = db.Column(db.String(20), nullable=False, unique=True)
    runtime = db.Column(db.String(20), nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    director = db.Column(db.String(100), nullable=True)

    __tablename__ = "movies"

    def __repr__(self):
        return f"<Movie {self.title}>"

    def __init__(
        self,
        title: str,
        year: int | None,
        imdb_id: str,
        runtime: str | None,
        genre: str | None,
        director: str | None,
    ):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.runtime = runtime
        self.genre = genre
        self.director = director

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "imdb_id": self.imdb_id,
            "runtime": self.runtime,
            "genre": self.genre,
            "director": self.director,
        }

    @classmethod
    def from_open_movie_db(cls, data: dict):
        title = data.get("Title")
        if title is None:
            raise ValueError("Title is required")
        if type(title) is not str:
            raise ValueError("Title must be a string")
        year = data.get("Year")
        if year is None:
            raise ValueError("Year is required")

        if type(year) is not int:
            if type(year) is str:
                year = int(year[:4])
            else:
                raise ValueError(
                    "Year must be an integer or a string that can be converted to an integer"
                )
        imdb_id = data.get("imdbID")
        if imdb_id is None:
            raise ValueError("imdbID is required")
        runtime = data.get("Runtime")
        genre = data.get("Genre")
        director = data.get("Director")
        return cls(title, year, imdb_id, runtime, genre, director)
