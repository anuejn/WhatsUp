import time
import re

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import feedparser


def push_article(collection, article):
        try:
            collection.insert_one(article)
            print("add %s" % article["_id"])
        except DuplicateKeyError:
            pass  # article is already in db


# initialize the database connection
client = MongoClient(host="mongodb")
collection = client.whatsup.news

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
            push_article(collection, article)

        last_updated = utime

    time.sleep(10)  # check every 10 seconds
