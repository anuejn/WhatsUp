# MongoHttp
The mongoDB HTTP wrapper is writen in python. It allows us to make unauthenticated
map/reduce requests to a Mongodb via HTTP, which is not possible by default. . It exposes a single simple
HTTP GET endpoint:
```
GET /?map=[mapfunction]&reduce=[reducefunction]
```
This endpoint returns the result of the map/reduce request as given by the DB.
