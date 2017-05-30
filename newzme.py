import cgitb
import datetime
import json
import time
import feedprocessor
import firebasestorage
from newsplease import NewsPlease

import logging
logging.basicConfig(filename='newzme.log',level=logging.WARNING)

cgitb.enable()

print("Content-Type: text/html")


feeds = json.load(open("feeds.json"))
fp = feedprocessor.FeedProcessor("stopwords.json", logging)
stor = firebasestorage.FirebaseStorage(logging)


def process(feed):
    listOfURLS = []
    startRSS = time.time()
    articles = fp.process(feed, stor.feed_exists)
    articleList = []
    print("<p>Starting reading: " + feed["name"] + "</p>")
    for article in articles:
        if article == False:
            continue
        articleList.append(article)
        listOfURLS.append(article["link"])
    totalRSS = time.time() - startRSS
    print("RSS Scrape lasted %s seconds" % (totalRSS))
    numOfURLS = len(listOfURLS)
    print("Started Scrape")
    startCrawl = time.time()
    groupArtResp = NewsPlease.from_urls(listOfURLS)
    groupResList = list(groupArtResp.values())
    totalCrawl = time.time() - startCrawl
    print("Scrape of %s urls lasted %s seconds" % (numOfURLS, totalCrawl))
    urlCount = 0
    for urlCount in range(len(groupArtResp)):
        x = 0
        for x in range(len(articleList)):
            if articleList[x]['link'] == groupResList[urlCount]['url']:
                articlePre1 = groupResList[urlCount]['text']
                articlePre15 = str(articlePre1).replace("Advertisement Continue reading the main story\n", "")
                articlePre2 = articlePre15.replace("Photo\n", "")
                articleList[x]['words'] = articlePre2
                articleList[x]['image'] = groupResList[urlCount]['image']
                dt = datetime.datetime.utcnow()
                article_prepared = {"feed": feed, "article": articleList[x], "timestamp": dt}
                stor.save(article_prepared)
                break

    del groupResList[:]
    articleList.clear()
    listOfURLS.clear()
    del listOfURLS[:]
    del articleList[:]
    print("<p>Success saving: " + feed["name"] + "</p>")



for i in range(len(feeds)):
    process(feeds[i])
