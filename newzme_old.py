#!/usr/bin/python

import urllib.request
import urllib.error
import feedparser
import json
import cgitb

cgitb.enable()

print("Content-Type: text/html")
print()

firebase_url = "https://newzme-34c77.firebaseio.com/news_data.json"

feeds = list()
feeds.append("https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/technology/rss.xml")
feeds.append("http://rss.nytimes.com/services/xml/rss/nyt/Books.xml")
feeds.append("http://rss.nytimes.com/services/xml/rss/nyt/Business.xml")
feeds.append("http://rss.nytimes.com/services/xml/rss/nyt/Fashion.xml")
feeds.append("http://feeds.feedburner.com/variety/headlines")
feeds.append("http://www.mtv.com/rss/news/news_full.jhtml")
feeds.append("http://rss.sciam.com/ScientificAmerican-Global")
feeds.append("http://feeds.foxnews.com/foxnews/latest")
feeds.append("http://feeds.reuters.com/reuters/topNews")
feeds.append("http://rss.cnn.com/rss/edition.rss")
feeds.append("https://www.wired.com/feed/")
feeds.append("https://www.cnet.com/rss/news/")
feeds.append("http://feeds.washingtonpost.com/rss/business")
feeds.append("http://feeds.gawker.com/gizmodo/full")
feeds.append("http://www.fool.com/a/feeds/foolwatch?format=rss2&id=foolwatch&apikey=foolwatch-feed")
feeds.append("http://news.nationalgeographic.com/index.rss")

feed_index = 0
whitelist = set('abcdefghijklmnopqrstuvwxy ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

def parse_feed(url):

    try:
        rss_loader = feedparser.parse(url)
    except Exception as e:
        print("Error")
        parse_next()
    else:
        index = 1
        master_list = dict()

        for child in rss_loader.entries:
            article = dict()
            article["words"] = dict()
            article["title"] = child["title"]
            article["link"] = child["link"]

            if "description" in child:
                article["summary"] = child["description"]
                my_string = child["description"]
            else:
                my_string = ""

            my_string = ''.join(filter(whitelist.__contains__, my_string))
            words_list = my_string.replace(",", "").replace(".", "").split(" ")

            for word in words_list:
                if word != "":
                    article["words"][word] = words_list.count(word)

            master_list["article"+str(index)] = article
            index += 1

        json_data = json.dumps(master_list).encode()
        request = urllib.request.Request(firebase_url, data=json_data)

        try:
            urllib.request.urlopen(request)
        except urlib.error.URLError:
            parse_next()
        else:
            print("<p>Success parsing: " + str(feeds[feed_index]) + "</p>")
            parse_next()


def parse_next():

    global feed_index
    feed_index += 1

    if feed_index < len(feeds):
        parse_feed(feeds[feed_index])
    else:
        print("<p>All feeds have been processed.</p>")


parse_feed(feeds[feed_index])