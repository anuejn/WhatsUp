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
