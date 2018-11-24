#!/usr/bin/python3
import newspaper
from newspaper import Article
import nltk
import feedparser
from datetime import datetime, timedelta
import json

DATA_PATH = '/var/www/news/data.json'

def convertDate(timestruct):
    return datetime(*timestruct[:6])

news = []

feeds = {}
#feeds['nyt'] = {'name': 'The New York Times', 'link': 'http://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'lower_bound': 500}
feeds['nrc'] = {'name': 'NRC', 'link': 'https://nrc.nl/rss', 'lower_bound': 1200}
feeds['guardian'] = {'name': 'The Guardian', 'link': 'https://www.theguardian.com/world/rss', 'lower_bound': 1100}
feeds['volkskrant'] = {'name': 'De Volkskrant', 'link': 'https://www.volkskrant.nl/nieuws-achtergrond/rss.xml', 'lower_bound': 1300}
feeds['newyorker'] = {'name': 'The New Yorker', 'link': 'https://www.newyorker.com/feed/news', 'lower_bound': 2000}
feeds['groene'] = {'name': 'De Groene Amsterdammer', 'link': 'https://groene.nl/feed.atom', 'lower_bound': 1000}
feeds['fd'] = {'name': 'Het Financieele Dagblad', 'link': 'https://fd.nl/?rss', 'lower_bound': 1000}

count = 0
for org, src in feeds.items():
    feed = feedparser.parse(src['link'])

    for e in feed.entries:
        today = datetime.now()
        border = today - timedelta(days=1)
        try:
            t = convertDate(e.published_parsed)
        except Exception as ex:
            continue

        if t > border:
            a = Article(e.link)
            try:
                a.download()
                a.parse()
            except:
                continue

            if len(a.text.split()) > src['lower_bound']:
                print("[{}] {}".format(org, a.title))
                news.append({'source': src['name'], 'title': a.title, 'date': t, 'url': a.url, 'text': a.text.replace("\n", '<br>'), 'img': a.top_image})
                count += 1

print("Found {} articles".format(count))

with open(DATA_PATH, 'w') as out:
    json.dump(news, out, indent=4, sort_keys=True, default=str)
