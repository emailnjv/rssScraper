import cgitb
import datetime
import json
import feedprocessor
import firebasestorage
import newspaper
import requests

import logging
logging.basicConfig(filename='newzme.log',level=logging.WARNING)

cgitb.enable()

print("Content-Type: text/html")


feeds = json.load(open("/var/www/html/python-scripts/feeds.json"))
fp = feedprocessor.FeedProcessor("/var/www/html/python-scripts/stopwords.json", logging)
stor = firebasestorage.FirebaseStorage(logging)


def process(feed):
    articles = fp.process(feed, stor.feed_exists)
    articleList = []
    print("<p>Starting reading: " + feed["name"] + "</p>")
    for article in articles:
        if article == False:
            continue
        articleList.append(article)
        try:
            request = requests.get(article['link'])
            if request.status_code == 200:
                articleTest = newspaper.Article(article["link"], memoize_articles=False, follow_meta_refresh=True)
                articleTest.build()
                articlePreAA = articleTest.text
                articlePreA = articlePreAA.replace("Audio clip: Listen to audio clip.\n", "")
                articlePreB = articlePreA.replace('(CNN) ', '')
                articlePreC = articlePreB.replace('FILE PHOTO - ', '')
                articlePreD = articlePreC.replace('FBI logo (Photo: FBI)\n\n', '')
                articleTObj = {}
                articleTObj['keywords'] = articleTest.keywords
                articleTObj['words'] = articlePreD
                articleTObj['title'] = article['title'].title()
                articleTObj['summary'] = articleTest.summary
                articleTObj['image'] = articleTest.top_image
                articleTObj['link'] = article['link']
                if 'topics' in article:
                    articleTObj['topics'] = article['topics']
                if "tags" in article:
                    articleTObj['tags'] = article['tags']

                dt = datetime.datetime.utcnow()
                article_prepared = {"feed": feed, "article": articleTObj, "timestamp": dt}
                stor.save(article_prepared)

            else:
                print('Article Link Is Broken')
        except:
            print("Error acessing link " + article['link'])


    print("<p>Success saving: " + feed["name"] + "</p>")



for i in range(len(feeds)):
    process(feeds[i])
