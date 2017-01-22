from pymongo import MongoClient
from bson.code import Code
from flask import Flask, request, jsonify, abort

import json
import base64

# initialize the database connection
client = MongoClient(host="mongodb")
collection = client.whatsup.news

# init the flask server
app = Flask(__name__)


@app.route('/api')
def wrap():
    map_function = request.args.get('map')
    reduce_function = request.args.get('reduce')
    query = request.cookies.get('query')

    if reduce_function is None or map_function is None:
        return abort(400)

    map_function = str(map_function)
    reduce_function = str(reduce_function)

    if query:
        query = json.loads(base64.b64decode(query).decode("utf-8"))

    result = collection.map_reduce(Code(map_function), Code(reduce_function), out={"inline": 1}, query=query)

    return jsonify(result["results"])


# finally run the flask server
if __name__ == "__main__":
    app.run("0.0.0.0", 3141, debug=True)
