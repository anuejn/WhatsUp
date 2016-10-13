import time

from pymongo import MongoClient
import feedparser


def push_article(collection, article):
    if not collection.find_one(article):
        collection.insert_one(article)


# initialize the database connection
client = MongoClient()  # use default connection settings for now
db = client.news
spon = db.spon

# parse the feed
last_updated = 0
while True:
    feed = feedparser.parse("www.spiegel.de/index.rss")
    print(feed)
    utime = time.mktime(feed["feed"]["updated_parsed"])
    if utime > last_updated:
        print("news!")
        articles = feed["entries"]
        for article in articles:
            print(article["title"])
            push_article(spon, article)

        last_updated = utime

    time.sleep(10)  # check every 10 seconds
