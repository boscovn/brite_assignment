# Movies api

This is a rest api to manage movies.
Both the initial population and additional movies query the omdb api to get the movie information.
It uses an sql database to store the movies. SQLite is used for the development environment and PostgreSQL for the production environment.
It caches the get requests and invalidates the cache when a new movie is added or deleted.
To delete movies, the user must be authenticated.
