GET {{API_URL}}/
HTTP 200

GET {{API_URL}}/nonexistent
HTTP 404
#
GET {{API_URL}}/movies/
HTTP 200
[Asserts]
jsonpath "$.movies" count == 10
jsonpath "$.movies[0].title" == "They Live"
jsonpath "$.movies[0].imdb_id" == "tt0096256"
jsonpath "$.movies[1].title" == "When They See Us"
jsonpath "$.movies[1].imdb_id" == "tt7137906"
jsonpath "$.movies[2].title" == "The Harder They Fall"
jsonpath "$.movies[2].imdb_id" == "tt10696784"
jsonpath "$.movies[3].title" == "See How They Run"
jsonpath "$.movies[3].imdb_id" == "tt13640696"
jsonpath "$.movies[4].title" == "They Cloned Tyrone"
jsonpath "$.movies[4].imdb_id" == "tt9873892"
jsonpath "$.movies[5].title" == "They Shall Not Grow Old"
jsonpath "$.movies[5].imdb_id" == "tt7905466"
jsonpath "$.movies[6].title" == "They Call Me Trinity"
jsonpath "$.movies[6].imdb_id" == "tt0067355"
jsonpath "$.movies[7].title" == "They Came Together"
jsonpath "$.movies[7].imdb_id" == "tt2398249"
jsonpath "$.movies[8].title" == "In China They Eat Dogs"
jsonpath "$.movies[8].imdb_id" == "tt0180748"
jsonpath "$.movies[9].title" == "They Shoot Horses, Don't They?"
jsonpath "$.movies[9].imdb_id" == "tt0065088"

GET {{API_URL}}/movies/
[QueryStringParams]
per_page: 5
HTTP 200
[Asserts]
jsonpath "$.movies" count == 5


GET {{API_URL}}/movies/
[QueryStringParams]
page: 5
HTTP 200
[Asserts]
jsonpath "$.movies" count == 10

GET {{API_URL}}/movies/
[QueryStringParams]
per_page: 5
page: 2
HTTP 200
[Asserts]
jsonpath "$.movies" count == 5

POST {{API_URL}}/movies/add
{
	"title": "La Dolce Vita"
}
HTTP 201
[Captures]
dolce_vita_id: jsonpath "$.id"

GET {{API_URL}}/movies/{{dolce_vita_id}}
HTTP 200
[Asserts]
jsonpath "$.title" == "La Dolce Vita"
jsonpath "$.imdb_id" == "tt0053779"
jsonpath "$.director" == "Federico Fellini"
jsonpath "$.genre" == "Comedy, Drama"
jsonpath "$.release_date" == "19/04/1961"
jsonpath "$.runtime" == "174 min"
jsonpath "$.year" == 1960
jsonpath "$.poster" == "https://m.media-amazon.com/images/M/MV5BODQ0NzY5NGEtYTc5NC00Yjg4LTg4Y2QtZjE2MTkyYTNmNmU2L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg"

POST {{API_URL}}/movies/add
{
	"title": "La Dolce Vita"
}
HTTP 400

DELETE {{API_URL}}/movies/{{dolce_vita_id}}/delete
HTTP 401

POST {{API_URL}}/users/login
{
	"username": "admin",
	"password": "admin"
}
HTTP 200
[Captures]
access_token: jsonpath "$.access_token"

GET {{API_URL}}/users/check
Authorization: Bearer {{access_token}}
HTTP 200
[Asserts]
jsonpath "$.message" == "Hello admin"


DELETE {{API_URL}}/movies/{{dolce_vita_id}}/delete
Authorization: Bearer {{access_token}}
HTTP 204

DELETE {{API_URL}}/movies/{{dolce_vita_id}}/delete
Authorization: Bearer {{access_token}}
HTTP 404

GET {{API_URL}}/movies/10000
HTTP 404

GET {{API_URL}}/movies/{{dolce_vita_id}}
HTTP 404

POST {{API_URL}}/movies/add
{
	"title": "La escopeta nacional"
}
HTTP 201
[Captures]
escopeta_nacional_id: jsonpath "$.id"
[Asserts]
jsonpath "$.title" == "La escopeta nacional"

GET {{API_URL}}/movies/{{escopeta_nacional_id}}
HTTP 200
[Asserts]
jsonpath "$.title" == "La escopeta nacional"

POST {{API_URL}}/movies/add
{
	"title": "La escopeta nacional"
}
HTTP 400

POST {{API_URL}}/movies/add
{
	"year": 1978
}
HTTP 400


GET {{API_URL}}/movies/get_one
[QueryStringParams]
title: "Movie that does not exist"
HTTP 404


GET {{API_URL}}/movies/get_one
HTTP 404

POST {{API_URL}}/users/login
{
	"username": "admin",
	"password": "incorrect"
}
HTTP 403

POST {{API_URL}}/users/login
{
	"username": "nonexistent",
	"password": "incorrect"
}
HTTP 404

POST {{API_URL}}/users/login
{
	"password": "admin"
}
HTTP 400

POST {{API_URL}}/users/login
{
	"username": "admin"
}
HTTP 400
