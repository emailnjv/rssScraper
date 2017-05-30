import json
import urllib.request
import urllib.error


class Longman(object):
    longman_url = "http://api.pearson.com/v2/dictionaries/entries?{1}={0}&part_of_speech='noun'%2C'verb'"
    cache = "https://newzme-34c77.firebaseio.com/longman_api.json"


    def __init__(self, logging):
        self.logging = logging


    def __request(self, type, value):
        url = self.longman_url.replace("{0}", value).replace("{1}", type)

        request = urllib.request.Request(url)
        content = urllib.request.urlopen(request)
        jlong = content.read().decode("utf-8")
        return json.loads(jlong, "utf-8")

    def adjust_word(self, word):
        word = word.lower()
        longman = self.__request("headword", word)

        if longman["status"] != 200:
            return False

        if longman["count"] == 0:
            # return False
            return {"word": word, "part": ""}


        return {"word": longman["results"][0]["headword"], "part": longman["results"][0]["part_of_speech"]}

    def get_from_cache(self, word):
        url = self.cache + "?orderBy=\"word\"&equalTo=\"{0}\""
        url = url.replace("{0}", word)

        request = urllib.request.Request(url)
        content = urllib.request.urlopen(request)
        jsaved = content.read().decode("utf-8")
        saved = json.loads(jsaved, "utf-8")

        return saved

    def save_to_cache(self, content):
        json_data = json.dumps(content).encode()
        request = urllib.request.Request(self.cache, data=json_data)

        try:
            content = urllib.request.urlopen(request)
            return True
        except urllib.error.URLError:
            return False

    def get_synonyms(self, word):
        longman = self.__request("synonyms", word)

        if longman["status"] != 200:
            return False
        
        if longman["count"] == 0:
            return []

        words = []
        for result in longman["results"]:
            if "senses" in result.keys():
                if "synonym" in result["senses"][0].keys():
                    words.append(result["senses"][0]["synonym"].lower())
        
        return list(set(words))

    def get_related_words(self, word):
        longman = self.__request("related_words", word)

        if longman["status"] != 200:
            return False

        if longman["count"] == 0:
            return []

        words = []
        for result in longman["results"]:
            if "senses" in result.keys():
                if "related_word" in result["senses"][0].keys():
                    words.append(result["senses"][0]["related_word"].lower())
        
        return words

    def identify(self, req):
        """cache = self.get_from_cache(word)

        if cache:
            return cache
        """
        word = self.adjust_word(req)
        self.logging.debug("longman returns to: " + req + " -> " + word["part"] + " | " + word["word"])
        """
        if adjustedwWord:
            if adjustedwWord != word:
                cache = self.get_from_cache(word)
                if cache:
                    return cache

            word = adjustedwWord
        """
        #synonyms = []
        #related = []
        #if word["part"] == "noun":
        #    synonyms = self.get_synonyms(word["word"])
        #    related = self.get_related_words(word["word"])

        #content = {
        #    "word": word["word"].lower(),
        #    "synonyms": synonyms,
        #    "related": related
        #}
        if word["part"] == "noun":
            return word["word"].lower()
        
        #self.save_to_cache(content)

        return False