import time
import re

import couchdb
import feedparser


def push_article(db, article):
    try:
        db.save(article)
        print(article)
    except couchdb.http.ResourceConflict:
        pass  # article already in db


# initialize the database connection
server = couchdb.Server('http://admin:cOuChDb!1!@neindev.tk:5984/')
db = server["news"]

# parse the feed
last_updated = 0
while True:
    feed = feedparser.parse("http://newsfeed.zeit.de/index")
    utime = time.mktime(feed["updated_parsed"])
    if utime > last_updated:
        articles = feed["entries"]
        for raw_article in articles:
            article = {
                "title": raw_article["title"],
                "summary": re.sub("<[\s\S]*>", "", raw_article["summary"]),

                "meta": {
                    "source": "zeit",
                    "author": re.sub("ZEIT ONLINE: \w* - ", "", raw_article["author"]).split(", "),
                    "tags": list(map(lambda tag: tag["term"], raw_article["tags"])),
                    "timestamp": time.mktime(raw_article["published_parsed"]),
                    "url": raw_article["link"]
                },
                "_id": raw_article["link"]
            }
            push_article(db, article)

        last_updated = utime

    time.sleep(10)  # check every 10 seconds
