import pymongo
from pymongo import MongoClient

client = MongoClient()  # use default connection settings for now
db = client.news

test_article = {
    "title": "some title",
    "subtitle": "some subtitle",
    "text": "Lorem ipsum dolor sit atmet",

    # metadata
    "author": "Max Mustermann",
    "timestamp": "000000000",
    "category": "category/sub/sub"
}

spon = db.spon

spon.insert(test_article)
