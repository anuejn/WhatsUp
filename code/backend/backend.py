import couchdb
from flask import Flask, request, jsonify, abort

# init the couchdb connection
server = couchdb.Server('http://admin:cOuChDb!1!@neindev.tk:5984/')
db = server["news"]

# init the flask server
app = Flask(__name__)


@app.route('/')
def wrap():
    map_function = request.args.get('map')
    reduce_function = request.args.get('reduce')

    if reduce_function is None or map_function is None:
        return abort(400)

    print(str(map_function))
    print(str(reduce_function))

    result = db.query(str(map_function), str(reduce_function)).rows

    return jsonify(result)


# run the flask server
if __name__ == "__main__":
    app.run("0.0.0.0", 3141)
