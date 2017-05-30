from newsplease import NewsPlease
import time
class ScrapeHandler(object):
    def __init__(self, child):
        self.url = child.link


    def parseArticle(self):
        start = time.time()
        articleResponse = NewsPlease.from_url(self.url)
        article = dict()
        articlePre1 = articleResponse['text'].replace("Advertisement Continue reading the main story\n", "")
        articlePre2 = articlePre1.replace("Photo\n", "")
        article['words'] = articlePre2
        article['image'] = articleResponse['image']
        end = time.time() - start
        return article
