# Backend
THis directory contains a simple wrapper. It allows us to make unauthenticated 
map/reduce requests to a Couchdb, which is not possible by default. This is achieved
by having this script authenticated connected to the DB. It exposes a single simple
HTTP GET endpoint:
```
GET /?map=[mapfunction]&reduce=[reducefunction]
```
This endpoint returns the result of the map/reduce request as given by the DB.