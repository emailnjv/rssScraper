#!/usr/bin/python
import json
import datetime
import feedparser
import urllib.request
from scrapeHandler import ScrapeHandler
import re
import timeit
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

    def __get_keywords(self, text):
        my_string = text.lower()
        my_string = ''.join(filter(self.whitelist.__contains__, my_string))
        words_list = my_string.replace(",", "").replace(".", "").split(" ")
        words_list = list(set(words_list) - self.stopwords)

        words = []
        for word in filter(lambda w: w != "", words_list):
            acceptable = self.__acceptable_word(word)
            if acceptable:
                words.append(acceptable)

        return words

    def __parse(self, child, checkExists):
        article = dict()
        article["title"] = re.sub('\s+',' ',child["title"])
        article["link"] = child["link"]
        # if checkExists(article):
        #     self.logging.debug(article["link"] + "Exists... aborting")
        #     return False

        self.logging.debug(article["link"] + "DOnt exists, reading...")

        words_list = self.__get_keywords(article["title"])
        self.logging.debug("Keywords list: " + ", ".join(words_list))

        permid_content = article["title"]
        if "description" in child:
            article["summary"] = child["description"]
            permid_content = permid_content + " " + article["summary"]
            if not words_list:
                words_list = self.__get_keywords(article["summary"])
                self.logging.debug(
                    "summary Keywords list: " + ", ".join(words_list))

        permid_analyzed = self.permid.tag(permid_content)
        article["keywords"] = words_list + permid_analyzed["tags"]
        article["topics"] = permid_analyzed["topics"]
        article["likes"] = 0

        return article
