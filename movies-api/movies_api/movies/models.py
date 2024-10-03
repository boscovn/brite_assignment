from movies_api.utils import db
import datetime


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    imdb_id = db.Column(db.String(20), nullable=False, unique=True)
    runtime = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    poster = db.Column(db.String(200), nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    director = db.Column(db.String(100), nullable=True)

    __tablename__ = "movies"

    def __init__(
        self,
        title: str,
        imdb_id: str,
        year: int | None = None,
        runtime: int | None = None,
        genre: str | None = None,
        director: str | None = None,
        release_date: datetime.date | None = None,
        poster: str | None = None,
    ):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.release_date = release_date
        self.poster = poster

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "imdb_id": self.imdb_id,
            "runtime": f"{self.runtime} min" if self.runtime else None,
            "genre": self.genre,
            "director": self.director,
            "release_date": (
                self.release_date.strftime("%d/%m/%Y") if self.release_date else None
            ),
            "poster": self.poster,
        }

    @classmethod
    def from_open_movie_db(cls, data: dict):
        response = data.get("Response")
        if response == "False":
            raise ValueError("Movie not found in OMDB API")
        title = data.get("Title")
        if title is None:
            raise ValueError("Title is required")
        if type(title) is not str:
            raise ValueError("Title must be a string")
        year = data.get("Year")
        if type(year) is not int and year is not None:
            if type(year) is str:
                year = int(year[:4])
            else:
                year = None
        imdb_id = data.get("imdbID")
        if imdb_id is None:
            raise ValueError("imdbID is required")
        runtime = data.get("Runtime")
        if runtime is not None:
            try:
                runtime = int(runtime.split(" ")[0])
            except ValueError:
                runtime = None
        genre = data.get("Genre")
        director = data.get("Director")
        release_date = data.get("Released")
        poster = data.get("Poster")
        if release_date is not None:
            try:
                release_date = datetime.datetime.strptime(
                    release_date, "%d %b %Y"
                ).date()
            except ValueError:
                release_date = None

        return cls(
            title=title,
            year=year,
            imdb_id=imdb_id,
            runtime=runtime,
            genre=genre,
            director=director,
            release_date=release_date,
            poster=poster,
        )
