# Movies api

This is a rest api to manage movies.
Both the initial population and additional movies query the omdb api to get the movie information.
It uses an sql database to store the movies. SQLite is used for the development environment and PostgreSQL for the production environment.
It caches the get requests and invalidates the cache when a new movie is added or deleted.
To delete movies, the user must be authenticated.

# Endpoints

## GET /movies

Returns a list of all movies.
Takes the url parameters `page` and `per_page` to paginate the results.

## GET /movies/{id}

Returns a single movie. Where `{id}` is the id of the movie.

## GET /movies/get_one

Returns a single movie.
It must have the url parameter `title` with the title of the movie.

## POST /movies/add

Adds a movie to the database.
It must have the json body with the title of the movie in the format:
```json
{
    "title": "movie title"
}
```

## DELETE /movies/{id}/delete

Deletes a movie from the database. Where `{id}` is the id of the movie.


## POST /users/login

Logs in a user.
It must have the json body with the username and password in the format:
```json
{
    "username": "username",
    "password": "password"
}
```
