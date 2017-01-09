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


