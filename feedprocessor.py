#!/usr/bin/python
import json
import datetime
import feedparser
import urllib.request

from longman import Longman
from permid import Permid


class FeedProcessor(object):
    whitelist = set(
        'abcdefghijklmnopqrstuvwxy 0123456789')

    longman = {}
    permid = {}
    feeds = []
    stopwords = []

    def __init__(self, stopwords_json, logging):
        self.stopwords = set(json.load(open(stopwords_json)))
        self.logging = logging
        self.longman = Longman(logging)
        self.permid = Permid(logging)

    def __acceptable_word(self, word):
        return self.longman.identify(word)

    def process(self, feed, checkExists):
        rss = self.__get(feed["url"])

        if not rss:
            return

        for child in rss.entries:
            yield self.__parse(child, checkExists)

    def __get(self, url):
        try:
            self.logging.debug('Reading ' + url)
            return feedparser.parse(url)
        except Exception as e:
            return False



    def __parse(self, child, checkExists):
        article = dict()

        article["title"] = child["title"]
        article["link"] = child["link"]

        # if checkExists(article):
        #     self.logging.debug(article["link"] + "Exists... aborting")
        #     return False

        self.logging.debug(article["link"] + "Does'nt exists, reading...")


        permid_content = article["title"]

        try:
            permid_analyzed = self.permid.tag(permid_content)
            article["topics"] = permid_analyzed["topics"]
            article["likes"] = 0
        except:
            self.logging.debug("Error attempting permid on " + article["link"])

        return article
