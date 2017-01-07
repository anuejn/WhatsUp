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
                print(raw_article["link"])
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
