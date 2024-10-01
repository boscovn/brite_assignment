GET {{API_URL}}/
HTTP 200

GET {{API_URL}}/nonexistent
HTTP 404
#
GET {{API_URL}}/movies
HTTP 200
[Asserts]
jsonpath $.length == 2

