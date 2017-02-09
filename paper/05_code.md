## Quellcode
### dev.yml
```
version: '2'

services:
  backend:
    build: backend/
    links:
      - mongodb

  frontend:
    build: frontend/
    links:
      - backend
    ports:
      - "80:80"

  mongodb:
    image: "mongo:latest"
    ports:
        - "27027:27017"

```
### deploy.yml
```
version: '2'

services:
  data-collectors:
    build: data-collectors/
    links:
      - mongodb
    restart: always

  backend:
    build: backend/
    links:
      - mongodb

  frontend:
    build: frontend/
    links:
      - backend
    ports:
      - "80:80"

  mongodb:
    image: "mongo:latest"
    #ports:
    #    - "27027:27017"

```
### Makefile
```
default: dev

dev:
	docker-compose -f dev.yml up --build -d

deploy:
	DOCKER_HOST=tcp://212.47.231.85:2376 \
	DOCKER_MACHINE_NAME=deploy \
	docker-compose -f deploy.yml up --build -d

clean:
	docker-compose -f dev.yml down --remove-orphans

restore: dev
	mongorestore --port 27027 backup

count:
	cloc --exclude-dir=lib --exclude-lang=XML .

```
### README.md
```
# Technical setup
All the things are set-up using docker compose. To start the app type `docker-compose up` in this directory. For more technical information about the architecture, i suggest looking at the `docker-compose.yml` file.

```
### data-collectors/main.py
```
import os
import time

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def load_modules():
    modules = list(map(lambda path: __import__('modules.' + path[:-3], fromlist=['modules']),
                       filter(lambda path: path.endswith(".py"), os.listdir("modules"))))
    for module in modules:
        try:
            module.init()
        except AttributeError:
            pass
    return modules


def push_article(collection, article):
    try:
        collection.insert_one(article)
        print("add %s" % article["_id"])
    except DuplicateKeyError:
        pass  # article is already in db

if __name__ == "__main__":
    # initialize the database connection:
    client = MongoClient(host="mongodb")
    collection = client.whatsup.news

    # load the modules
    modules = load_modules()
    last_updated = {}

    # crawl newspapers
    while True:
        for module in modules:
            print(str(module) + ":")
            articles, feed_time = module.get_articles(last_updated.get(module, 0))
            last_updated[module] = feed_time

            # push the articles in the DB
            for article in articles:
                if not article["text"]:
                    print("fuck: " + article["_id"])
                    continue
                push_article(collection, article)
        print("crawling finished")
        time.sleep(60)



```
### data-collectors/requirements.txt
```
mongo
feedparser
pyquery

```
### data-collectors/Dockerfile
```
FROM python:3

COPY requirements.txt /code/
WORKDIR /code
RUN pip install -r requirements.txt

COPY . /code

CMD ["python", "-u", "main.py"]

```
### data-collectors/README.md
```
# Data collectors
This directory contains the data collectors. They collect data from different news sites and add it to the DB.

```
### data-collectors/article_structure.json
```
{
  "title": "required",
  "subtitle": "optional",
  "summary": "optional",
  "text": "optional",

  "meta": {
    "source": "required",
    "author": "optional",
    "tags": "optional",
    "timestamp": "optional",
    "url": "optional"
  }
}
```
### data-collectors/modules/bild.py
```
import feedparser
import time
from pyquery import PyQuery as pq
import re


def init():
    print("bild module loaded")


def get_articles(last_updated):
    articles = []
    feed = feedparser.parse("http://www.bild.de/rssfeeds/vw-alles/vw-alles-26970192,sort=1,view=rss2.bild.xml")
    feed_time = time.mktime(feed["feed"]["updated_parsed"])
    if feed_time > last_updated:
        raw_articles = feed["entries"]
        for raw_article in raw_articles:
            if "BILDplus Inhalt" in raw_article["summary"]:  # fuck bild plus
                continue
            page = pq(url=raw_article["link"])
            page("em").remove()
            page("style").remove()
            page("script").remove()

            article = {
                "title": raw_article["title"],
                "summary": re.sub("<[\s\S]*>", "", raw_article["summary"]),
                "text": page(".txt").text(),
                "raw": page.html(),

                "meta": {
                    "source": "bild",
                    "tags": list(map(lambda tag: tag["term"], raw_article["tags"])),
                    "timestamp": time.mktime(raw_article["published_parsed"]),
                    "url": raw_article["link"]
                },
                "_id": raw_article["link"]
            }
            if time.time() > article["meta"]["timestamp"] + 60*60*48:
                continue
            articles.append(article)

    return articles, feed_time

```
### data-collectors/modules/spon.py
```
import feedparser
import time
from pyquery import PyQuery as pq
import re


def init():
    print("spon module loaded")


def get_articles(last_updated):
    articles = []
    feed = feedparser.parse("http://www.spiegel.de/schlagzeilen/index.rss")
    feed_time = time.mktime(feed["feed"]["updated_parsed"])
    if feed_time > last_updated:
        raw_articles = feed["entries"]
        for raw_article in raw_articles:
            page = pq(url=raw_article["link"])
            if page(".obfuscated").text():  # fuck spiegel plus
                continue
            article = {
                "title": raw_article["title"],
                "summary": re.sub("<[\s\S]*>", "", raw_article["summary"]),
                "text": page(".article-section")("p").text(),
                "raw": page.html(),

                "meta": {
                    "source": "spon",
                    "tags": list(map(lambda tag: tag["term"], raw_article["tags"])),
                    "timestamp": time.mktime(raw_article["published_parsed"]),
                    "url": raw_article["link"]
                },
                "_id": raw_article["link"]
            }
            articles.append(article)

    return articles, feed_time

```
### data-collectors/modules/zeit.py
```
import feedparser
import time
from pyquery import PyQuery as pq
import re


def init():
    print("zeit module loaded")


def get_articles(last_updated):
    articles = []
    feed = feedparser.parse("http://newsfeed.zeit.de/index")
    feed_time = time.mktime(feed["updated_parsed"])
    if feed_time > last_updated:
        raw_articles = feed["entries"]
        for raw_article in raw_articles:
            text = ""
            cnt = 0
            while not text and cnt < 100:  # zeit.de sucks hard
                page = pq(url=raw_article["link"])
                text = page(".article-page")("p").text()
                cnt += 1
            if not text:
                print("fuck: " + raw_article["link"])
                continue
            article = {
                "title": raw_article["title"],
                "summary": re.sub("<[\s\S]*>", "", raw_article["summary"]),
                "text": text,
                "raw": page.html(),

                "meta": {
                    "source": "zeit",
                    "author": re.sub("ZEIT ONLINE: \w* - ", "", raw_article["author"]).split(", "),
                    "tags": list(map(lambda tag: tag["term"], raw_article["tags"])),
                    "timestamp": time.mktime(raw_article["published_parsed"]),
                    "url": raw_article["link"]
                },
                "_id": raw_article["link"]
            }
            articles.append(article)
    return articles, feed_time

```
### data-collectors/modules/focus.py
```
import feedparser
import time
from pyquery import PyQuery as pq
import re


def init():
    print("focus module loaded")


def get_articles(last_updated):
    articles = []
    feed = feedparser.parse("http://rss.focus.de/fol/XML/rss_folnews.xml")
    feed_time = time.mktime(feed["feed"]["updated_parsed"])
    if feed_time > last_updated:
        raw_articles = feed["entries"]
        for raw_article in raw_articles:
            page = pq(url=raw_article["link"])
            page("style").remove()
            page("script").remove()

            article = {
                "title": raw_article["title"],
                "summary": re.sub("<[\s\S]*>", "", raw_article["summary"]),
                "text": page(".textBlock").text(),
                "raw": page.html(),

                "meta": {
                    "source": "focus",
                    "tags": list(map(lambda tag: tag["term"], raw_article["tags"])),
                    "timestamp": time.mktime(raw_article["published_parsed"]),
                    "url": raw_article["link"]
                },
                "_id": raw_article["link"]
            }
            articles.append(article)

    return articles, feed_time

```
### data-collectors/modules/sz.py
```
import feedparser
import time
from pyquery import PyQuery as pq
import re


def init():
    print("sz module loaded")


def get_articles(last_updated):
    articles = []
    feed = feedparser.parse("http://rss.sueddeutsche.de/app/service/rss/alles/index.rss?output=rss")
    feed_time = time.mktime(feed["feed"]["updated_parsed"])
    if feed_time > last_updated:
        raw_articles = feed["entries"]
        for raw_article in raw_articles:
            page = pq(url=raw_article["link"])
            page("style").remove()
            page("script").remove()
            page(".authorProfileContainer").remove()
            page(".ad").remove()
            page(".feedbackClick").remove()

            article = {
                "title": raw_article["title"],
                "summary": re.sub("<[\s\S]*>", "", raw_article["summary"]),
                "text": page("#article-body").text(),
                "raw": page.html(),

                "meta": {
                    "source": "sz",
                    "tags": list(map(lambda tag: tag["term"], raw_article["tags"])),
                    "timestamp": time.mktime(raw_article["published_parsed"]),
                    "url": raw_article["link"]
                },
                "_id": raw_article["link"]
            }
            articles.append(article)

    return articles, feed_time

```
### backend/requirements.txt
```
flask
mongo

```
### backend/Dockerfile
```
FROM python:3

COPY requirements.txt /code/
WORKDIR /code
RUN pip install -r requirements.txt

COPY . /code

CMD ["python", "-u", "mongo_http.py"]

```
### backend/mongo_http.py
```
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
    if "query" in request.args:
        query = request.args.get('query')
    else:
        query = request.cookies.get('query')

    if reduce_function is None or map_function is None:
        return abort(400)

    map_function = str(map_function)
    reduce_function = str(reduce_function)

    if query and str(query) != "":
        query = json.loads(base64.b64decode(str(query)).decode("utf-8"))
    else:
        query = {}

    result = collection.map_reduce(Code(map_function), Code(reduce_function), out={"inline": 1}, query=query)

    return jsonify(result["results"])


# finally run the flask server
if __name__ == "__main__":
    app.run("0.0.0.0", 3141, debug=True)

```
### backend/README.md
```
# MongoHttp
The mongoDB HTTP wrapper is writen in python. It allows us to make unauthenticated
map/reduce requests to a Mongodb via HTTP, which is not possible by default. . It exposes a single simple
HTTP GET endpoint:
```
GET /?map=[mapfunction]&reduce=[reducefunction]
```
This endpoint returns the result of the map/reduce request as given by the DB.

## Example
```
map:
function(doc) {

}

reduce:
function() {

}
```
```
### frontend/index.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Was ist los?</title>

    <style>
        body, html {
            width: 100%;
            height: 100%;

            box-sizing: border-box;

            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
        }
        a {
            box-sizing: border-box;
            flex-grow: 1;
            background-size: cover;
            display: inline-block;
            position: relative;

            min-width: 500px;
            min-height: 500px;
        }

        a:hover {
            box-shadow: 0 0 30px #0087AF;
            z-index: 10;
        }
    </style>
</head>
<body>
    <a href="visuals/table.html" style="background-image: url(img/table.png)"></a>
    <a href="visuals/cloud.html" style="background-image: url(img/cloud.png)"></a>
    <a href="visuals/force.html" style="background-image: url(img/force.png)"></a>

    <a href="visuals/time.html?q=wort" style="background-image: url(img/time.png)"></a>
    <a href="visuals/time_d.html?q=wort" style="background-image: url(img/time.png)"></a>

    <a href="visuals/contains.html?q=wort" style="background-image: url(img/contains.png)"></a>
    <a href="visuals/match.html?q=wort" style="background-image: url(img/contains.png)"></a>

    <a href="settings.html" style="background-image: url(img/settings.svg)"></a>
</body>
</html>

```
### frontend/settings.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Was ist los?</title>

    <script src="js/mongo_query.js"></script>
    <script>

        // fill the form
        function map() {
            emit(this.meta.source, 0)
        }

        function render(res) {
            var newspapers = res.map(e => e["_id"]);

            var checkboxHtml = newspapers.map(e => '<label for="' + e + '">' + e + '</label><input type="checkbox" id="' + e + '"><br>');
            document.getElementById("newspapers").innerHTML = checkboxHtml.reduce((a, b) => a + b);

            Array.from(document.getElementsByTagName("input")).forEach(el => el.onchange = () => {
                var from = document.getElementById("from").value;
                var to = document.getElementById("to").value;

                from = +new Date(from) / 1000;
                to = +new Date(to) / 1000;

                var sources = newspapers.filter(elem => document.getElementById(elem).checked);

                var query = {
                    "meta.timestamp": {"$gte": from},
                    "meta.timestamp": {"$lte": to},

                    "meta.source": {"$in": sources}
                };

                if (!(sources && from && to)) return;

                var base64 = btoa(JSON.stringify(query));
                console.log(base64);
                console.log(query);

                document.cookie = "query=" + base64 + "; path=/";


                alert("saved!");
            })
        }

        mongo_query(map, count, render, false);
    </script>
</head>
<body>
    <form>
        <p>
            <label for="from">from:</label><input type="datetime-local" id="from"></br>
            <label for="to">to:</label><input type="datetime-local" id="to">
        </p>
        <p id="newspapers">
            <!-- this is autogenerated -->
        </p>
    </form>
</body>
</html>

```
### frontend/nginx.conf
```
###############################################################
# this config file will be placed inside the docker container #
###############################################################

server {
    listen       80;
    server_name  localhost;

    # serve static files
    location / {
        root   /usr/share/nginx/html;
        index  index.html;

        # do nothing it the extension is already present
        if ($request_filename ~* ^.+.html$) {
          break;
        }

        # add .html if it was not present
        if (-e $request_filename.html) {
          rewrite ^/(.*)$ /$1.html permanent;
          break;
        }
    }

    # pass requests for dynamic content to the mongo_http API
    location /api {
      add_header Access-Control-Allow-Origin *;
      proxy_pass      http://backend:3141;
      proxy_read_timeout 60m;
    }

    # error pages
    error_page  404 /404.html;
    error_page   500 502 503 504  /50x.html;

    # i do wanted GET for everything...
    large_client_header_buffers 4 8M;
}

```
### frontend/Dockerfile
```
FROM nginx:latest
COPY nginx.conf etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html


```
### frontend/js/word_merge.js
```
/**
 * Created by jaro on 22.12.16.
 */

function word_merge(list) {
    modList = list.slice();
    modList.forEach((nowItem, nowCount, nowObject) => {
        var regex = new RegExp("^" + nowItem["_id"] + '.{0,2}','g');
        nowObject.forEach((item, index, object) => {
            if(nowItem["_id"] == item["_id"]) return;
            if(nowItem["_id"].length < 4) return;
            checkWord = item["_id"];
            if(checkWord.match(regex)) {
                nowObject[nowCount]["value"] += item["value"];
                object.splice(index, 1);
            }
        });
    });
    return modList
}

```
### frontend/js/mongo_query.js
```
/**
 * Created by jaro on 13.11.16.
 */
var host = document.location.host.indexOf(":") != -1 ? "http://localhost" : "";

function mongo_query(map, reduce, callback, query) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };

    var requestUrl = host + "/api";
    requestUrl += "?map=" + encodeURIComponent(map.toString());
    requestUrl += "&reduce=" + encodeURIComponent(reduce.toString());
    if(query && (typeof query === 'string' || query instanceof String)) {
        requestUrl += "&query=" + encodeURIComponent(query.toString());
    } else if(typeof(query) === "boolean"){
        requestUrl += "&query";
    }

    request.open("GET", requestUrl, true);
    request.send();
}

function example_map() {
    emit("count", 1);
}

function example_reduce(key, values) {
    return values.reduce((previousValue, currentValue) => currentValue + previousValue);
} 
var count = example_reduce;

```
### frontend/visuals/cloud.html
```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="../lib/d3.v3.js"></script>
    <script src="../lib/d3.layout.cloud.js"></script>

    <script src="../js/mongo_query.js"></script>
    <script src="../lib/stopwords.js"></script>
    <script src="../js/word_merge.js"></script>

    <script src="../params/cloud/first.js"></script>
    <script>
        window.onload = () => {
            function map() {
                var words = this.text.replace(/[^A-Za-zÄäÖöÜüß ]/g, " ").split(" ");
                for (var i = 0; i < words.length; i++) {
                    var word = words[i];
                    if(word) {
                        emit(words[i], 1);
                    }
                }
            }

            mongo_query(map, count, render);
        };

        var render = (wordList) => {
            wordList = word_merge(wordList
                    .filter(word => stopwords.indexOf(word["_id"].toLowerCase()) < 0)
                    .filter(word => german_stopwords_case.indexOf(word["_id"]) < 0)
                    .sort((a,b) => b["value"] - a["value"])
                    .slice(0, num_words)
            ).map(elem => {
                return {text: elem["_id"], size: elem["value"] / wordList[0]["value"] * text_multiply};
            }).sort((a,b) => b["value"] - a["value"]);
            console.log(wordList);
            var layout = d3.layout.cloud()
                    .size([window.innerWidth, window.innerHeight])
                    .words(wordList)
                    .padding(padding)
                    .rotate(() => 0)
                    .font("Serif")
                    .fontSize(d => d.size)
                    .on("end", draw);

            layout.start();

            function draw(words) {
                d3.select("body").append("svg")
                        .attr("width", layout.size()[0])
                        .attr("height", layout.size()[1])
                        .append("g")
                        .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
                        .selectAll("text")
                        .data(words)
                        .enter().append("text")
                        .style("font-size", d => d.size + "px")
                        .style("font-family", "Serif")
                        .attr("text-anchor", "middle")
                        .attr("transform", d => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")")
                        .text(d =>  d.text);
            }

        };
    </script>
</head>
<body>

</body>
</html>

```
### frontend/visuals/force.html
```
<!doctype html>
<html>

<head>
    <meta charset="utf-8">

    <title>Visualizer | Word Table</title>

    <style type="text/css" media="screen">
        html, body, svg {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }

        text {
            text-anchor: middle;
            font-family: Serif;
        }
    </style>
    <script src="../js/mongo_query.js"></script>
    <script src="../lib/stopwords.js"></script>
    <script src="../js/word_merge.js"></script>
    <script type="text/javascript" src="../lib/vivagraph.min.js"></script>

    <script src="../params/force/first.js"></script>
    <script>
        words = [];
        links = [];

        function zeroStage() {
            var map = function () {
                var words = this.text.replace(/[^A-Za-zÄäÖöÜüß ]/g, " ").split(" ");
                for (var i = 0; i < words.length; i++) {
                    var word = words[i];
                    if(word) {
                        emit(words[i], 1);
                    }
                }
            };
            mongo_query(map, count, firstStage);
        }
        function firstStage(inWords) {
            words = word_merge(
                inWords
                    .filter(word => stopwords.indexOf(word["_id"].toLowerCase()) < 0)
                    .filter(word => german_stopwords_case.indexOf(word["_id"]) < 0)
                    .filter(word => word["_id"][0].toUpperCase() == word["_id"][0])
                    .sort((a,b) => b["value"] - a["value"])
                    .slice(0, num_nodes)
            ).filter(word => stopwords.indexOf(word["_id"].toLowerCase()) < 0)
            .filter(word => german_stopwords_case.indexOf(word["_id"]) < 0)
            .sort((a,b) => b["value"] - a["value"]);

            var map = function() {
                var givenWords = __marker__;
                var distance_function = __marker2__;
                var words = this.text.replace(/[^A-Za-zÄäÖöÜüß ]/g, " ").split(" ").filter(w => w);

                // create dict with {"word": ['o', 'c', 'c', 'u', 'r', 'e', 'n', 'c', 'e']}
                var wordOccurrences = {};
                givenWords.forEach(word => {
                    var occurrences = [];
                    for(var i = 0; i < words.length; i++) {
                        if(word == words[i]) {
                            occurrences.push(i);
                        }
                    }
                    wordOccurrences[word] = occurrences;
                });

                givenWords.forEach(w => {
                    givenWords.forEach(v => { // every word combination is covered as w and v
                        if(w != v && wordOccurrences[w] && wordOccurrences[v]) {
                            list = [];
                            wordOccurrences[w].forEach(n => {
                                wordOccurrences[v].forEach(m => {
                                    list.push(distance_function(n, m));
                                });
                            });

                            strength = list.reduce((a, b) => a + b, 0);
                            if(strength != 0) {
                                arr = [w, v].sort();
                                emit(arr[0] + "." + arr[1], JSON.stringify([strength, 1]));
                            }
                        }
                    });
                });
            };

            var reduce = function (key, values) {
                var vals = values.map(val => JSON.parse(val));
                var newVals = vals[0].map((e, i) => e + vals[1][i]);
                return JSON.stringify(newVals);
            };

            map = map.toString().replace("__marker__", JSON.stringify(words.map(obj => obj["_id"])));
            map = map.replace("__marker2__", distance_function.toString());
            mongo_query(map, reduce, secondStage);
        }
        function secondStage(links_param) {
            links = links_param.map(link => {
                link["value"] = JSON.parse(link["value"]);
                return link;
            }).map(link => {
                link["value"] = link["value"][0];
                return link;
            });
            render();
        }
        function render() {
            var graph = Viva.Graph.graph();

            words.forEach(obj => {
                graph.addNode(obj["_id"], max_node_size * obj["value"] / Math.max.apply(Math, Object.keys(words).map(a => words[a]["value"])));
            });

            // one link per node
            lnks = {};
            links.forEach(link => {
                var words = link["_id"].split(".");
                if(!lnks[words[0]]) {
                    lnks[words[0]] = Object.keys(Object.keys)
                }
                lnks[words[0]].push([words[1], link["value"]]);
            });
            Object.keys(lnks).forEach(key =>
                lnks[key] = lnks[key].sort((a, b) => a[1] - b[1]).splice(0, num_min_links)
            );
            Object.keys(lnks).forEach(key => {
                start = key;
                lnks[key].forEach(end => {
                    graph.addLink(start, end[0], end[1])
                });
            });

            // top x nodes
            links.sort((l, m) => {
                return l["value"] - m["value"];
            }).splice(0, num_top_links).forEach(link => {
                var words = link["_id"].split(".");
                graph.addLink(words[0], words[1], link["value"])
            });

            var graphics = Viva.Graph.View.svgGraphics();
            graphics.node(function(node) {
                return Viva.Graph.svg('text')
                        .attr("font-size", node.data)
                        .attr("dy", ".25em")
                        .text(node.id);
            });

            graphics.link(function(link){
                return Viva.Graph.svg('path')
                        .attr('stroke', '#eee')
                        .attr('stroke-dasharray', '5, 5');
            }).placeLink(function(linkUI, fromPos, toPos) {
                // linkUI - is the object returend from link() callback above.
                var data = 'M' + fromPos.x + ',' + fromPos.y +
                        'L' + toPos.x + ',' + toPos.y;
                // 'Path data' (http://www.w3.org/TR/SVG/paths.html#DAttribute )
                // is a common way of rendering paths in SVG:
                linkUI.attr("d", data);
            });



            var layout = Viva.Graph.Layout.forceDirected(graph, layout_params);

            var renderer = Viva.Graph.View.renderer(graph, {
                graphics : graphics,
                layout : layout
            });
            renderer.run();
        }

        window.onload = zeroStage;
    </script>
</head>

<body>
</body>

</html>

```
### frontend/visuals/match.html
```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">

    <script src="../js/mongo_query.js"></script>

    <script src="../lib/Chart.bundle.min.js" integrity="sha256-RASNMNlmRtIreeznffYMDUxBXcMRjijEaaGF/gxT6vw=" crossorigin="anonymous"></script>
    <script>
        newspaperWords = [];
        actualWords = [];

        var stage1 = () => {
            function map() {
                this.text
                        .replace(/[^A-Za-zÄäÖöÜüß ]/g, " ")
                        .split(" ")
                        .filter(w => w)
                        .forEach(word => emit(this.meta.source, 1));
            }

            mongo_query(map, count, res => newspaperWords = res);
            stage2();
        };

        var stage2 = () => {
            function map() {
                this.text
                        .replace(/[^A-Za-zÄäÖöÜüß ]/g, " ")
                        .split(" ")
                        .filter(w => w)
                        .filter(w => /__marker__/i.test(w))
                        .forEach(word => emit(this.meta.source, 1));
            }

            map = map.toString().replace("__marker__", decodeURIComponent(location.href.split("?q=")[1]));

            mongo_query(map, count, render);
        };



        var render = (res) => {
            actualWords = res;

            var data = {
                labels: newspaperWords.map(e => e["_id"]),
                datasets: [
                    {
                        label: "%",
                        data: newspaperWords.map((e, i) => actualWords[i].value / e.value * 100),
                    }
                ]
            };

            var ctx = "myChart";

            var myBarChart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });
        };
        window.onload = stage1;
    </script>
</head>
<body>
    <canvas id="myChart"></canvas>
</body>
</html>

```
### frontend/visuals/contains.html
```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">

    <script src="../js/mongo_query.js"></script>

    <script src="../lib/Chart.bundle.min.js" integrity="sha256-RASNMNlmRtIreeznffYMDUxBXcMRjijEaaGF/gxT6vw=" crossorigin="anonymous"></script>
    <script>
        newspaperWords = [];
        actualWords = [];

        var stage1 = () => {
            function map() {
                        emit(this.meta.source, 1);
            }

            mongo_query(map, count, res => newspaperWords = res);
            stage2();
        };

        var stage2 = () => {
            function map() {
                if(/__marker__/i.test(this.text)) {
                    emit(this.meta.source, 1);
                }
            }

            map = map.toString().replace("__marker__", decodeURIComponent(location.href.split("?q=")[1]));

            mongo_query(map, count, render);
        };



        var render = (res) => {
            actualWords = res;

            var data = {
                labels: newspaperWords.map(e => e["_id"]),
                datasets: [
                    {
                        label: "%",
                        data: newspaperWords.map((e, i) => {
                            try {
                                return actualWords[i].value / e.value * 100;
                            } catch(e) {
                                return 0;
                            }
                        }),
                    }
                ]
            };

            var ctx = "myChart";

            var myBarChart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });
        };
        window.onload = stage1;
    </script>
</head>
<body>
    <canvas id="myChart"></canvas>
</body>
</html>

```
### frontend/visuals/time.html
```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="../lib/d3.v3.js"></script>
    <script src="../lib/d3_timeseries.js"></script>
    <link rel="stylesheet" href="../lib/d3_timeseries.css">

    <script src="../js/mongo_query.js"></script>
    <script>
        data = {};

        window.onload = () => {
            function map() {
                if(this.meta.timestamp < 1483228800) {
                    return;
                }
                var words = this.text.replace(/[^A-Za-zÄäÖöÜüß ]/g, " ").split(" ");
                words.forEach(word => {
                    if(/__marker__/i.test(word)) {
                        emit(new Date(this.meta.timestamp * 1000).toISOString().slice(0, 13) + "." + this.meta.source, 1);
                    }
                });
            }
            map = map.toString().replace("__marker__",  decodeURIComponent(location.href.split("?q=")[1]));
            mongo_query(map, count, render);
        };

        window.addEventListener("resize", render);
        var render = (wordList) => {
            data = {};
            wordList.map(elem => {
                var source = data[elem["_id"].split(".")[1]];
                if(!source) {
                    source = [];
                }
                source.push({date: new Date(elem["_id"].split(".")[0] + ":00"), n: elem["value"]});
                data[elem["_id"].split(".")[1]] = source;
            });
            console.log(data);

            var chart = d3.timeseries()
                    .margin.left(90)
                    .yscale.domain([0])

            Object.keys(data).forEach(key => {
                chart.addSerie(data[key], {x:'date',y:'n'}, {interpolate:'linear', label: key})
            });
            chart('#chart')

        };
    </script>
</head>
<body>
    <div id="chart"></div>
</body>
</html>

```
### frontend/visuals/table.html
```
<!doctype html>
<html>

<head>
    <meta charset="utf-8">

    <title>Visualizer | Word Table</title>

    <script src="../js/mongo_query.js"></script>
    <script src="../lib/stopwords.js"></script>
    <script src="../js/word_merge.js"></script>

</head>

<body>
    <main id="out">
        <!--the actual content goes here -->
        <script>
            function map() {
                var words = this.text.replace(/[^A-Za-zÄäÖöÜüß ]/g, " ").split(" ");
                for (var i = 0; i < words.length; i++) {
                    var word = words[i];
                    if(word) {
                      emit(words[i], 1);
                    }
                }
            }

            function render(obj) {
                obj = word_merge(obj
                                .filter(word => stopwords.indexOf(word["_id"].toLowerCase()) < 0)
                                .filter(word => german_stopwords_case.indexOf(word["_id"]) < 0)
                                .sort((a,b) => b["value"] - a["value"])
                                .slice(0, 500)
                ).sort((a,b) => b["value"] - a["value"]);

                var table = "<table style='margin: auto;'>";
                table += "<tr><th>word</th><th>count</th></tr>";
                obj.forEach(elm => {
                    table += "<tr><td>" + elm["_id"] + "</td><td>" + elm["value"] + "</td></tr>";
                });
                table += "</table>";

                document.getElementById("out").innerHTML = table;

                data = obj;
            }

            var data = [];
            mongo_query(map, count, render);
        </script>

        <!-- first place a loading animation here -->
        <img src="../img/loading.svg" alt="loading..." class="loading"/>
    </main>
</body>

</html>

```
### frontend/visuals/time_d.html
```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="../lib/d3.v3.js"></script>
    <script src="../lib/d3_timeseries.js"></script>
    <link rel="stylesheet" href="../lib/d3_timeseries.css">

    <script src="../js/mongo_query.js"></script>
    <script>
        data = {};

        window.onload = () => {
            function map() {
                if(this.meta.timestamp < 1483228800) {
                    return;
                }
                var words = this.text.replace(/[^A-Za-zÄäÖöÜüß ]/g, " ").split(" ");
                words.forEach(word => {
                    if(/__marker__/i.test(word)) {
                        emit(new Date(this.meta.timestamp * 1000).toISOString().slice(0, 10) + "." + this.meta.source, 1);
                    }
                });
            }
            map = map.toString().replace("__marker__",  decodeURIComponent(location.href.split("?q=")[1]));
            mongo_query(map, count, render);
        };

        window.addEventListener("resize", render);
        var render = (wordList) => {
            data = {};
            wordList.map(elem => {
                var source = data[elem["_id"].split(".")[1]];
                if(!source) {
                    source = [];
                }
                source.push({date: new Date(elem["_id"].split(".")[0]), n: elem["value"]});
                data[elem["_id"].split(".")[1]] = source;
            });
            console.log(data);

            var chart = d3.timeseries()
                    .margin.left(90)
                    .yscale.domain([0])

            Object.keys(data).forEach(key => {
                chart.addSerie(data[key], {x:'date',y:'n'}, {interpolate:'linear', label: key})
            });
            chart('#chart')

        };
    </script>
</head>
<body>
    <div id="chart"></div>
</body>
</html>

```
### frontend/params/cloud/first.js
```
/**
 * Created by jaro on 08.01.17.
 */

var num_words = 150;
var text_multiply = 20;
var padding = 2;

```
### frontend/params/force/first.js
```
/**
 * Created by jaro on 07.01.17.
 */

var num_nodes = 200;
var max_node_size = 50;
var distance_function = (a, b) => 1.0 / Math.pow(Math.abs(a - b), 0.001);
var num_min_links = 2;
var num_top_links = num_nodes;
var layout_params = {
    /**
     * Ideal length for links (springs in physical model).
     */
    springLength: 35,

    /**
     * Hook's law coefficient. 1 - solid spring.
     */
    springCoeff: 0.0008,

    /**
     * Coulomb's law coefficient. It's used to repel nodes thus should be negative
     * if you make it positive nodes start attract each other :).
     */
    gravity: -2.5,

    /**
     * Theta coefficient from Barnes Hut simulation. Ranged between (0, 1).
     * The closer it's to 1 the more nodes algorithm will have to go through.
     * Setting it to one makes Barnes Hut simulation no different from
     * brute-force forces calculation (each node is considered).
     */
    theta: 1,

    /**
     * Drag force coefficient. Used to slow down system, thus should be less than 1.
     * The closer it is to 0 the less tight system will be.
     */
    dragCoeff: 0.03,

    /**
     * Default time step (dt) for forces integration
     */
    timeStep : 5,

    /**
     * Maximum movement of the system which can be considered as stabilized
     */
    stableThreshold: 0.09
};

```

