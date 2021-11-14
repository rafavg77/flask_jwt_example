# flask_jwt_example

curl -X POST http://localhost:5000/auth -H 'Content-Type: application/json' -d '{"username":"user","password":"12345"}'
curl http://localhost:5000/protected -H 'Authorization: jwt <jwt>
