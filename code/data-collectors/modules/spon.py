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
