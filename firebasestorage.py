import hashlib
import json
import urllib.request
import urllib.error

#   TODO CHANGE FIREBASE URL
class FirebaseStorage(object):
    # https://newzme-34c77.firebaseio.com/news_data.json
    url = "https://freelance-test-455d9.firebaseio.com/news_data.json"

    def __init__(self, logging):
        self.logging = logging


    def hash(self, article):
        bytesarr = bytearray(article["link"], "utf-8")
        return hashlib.sha1(bytesarr).hexdigest()

    def __prepare(self, article):
        ts = article["timestamp"].isoformat()

        prepared = article["article"]
        prepared["feed"] = article["feed"]
        prepared["timestamp"] = ts
        prepared["hash"] = self.hash(prepared)

        return prepared

    def feed_exists(self, article):
        url = self.url + "?orderBy=\"hash\"&equalTo=\"{0}\""
        url = url.replace("{0}", self.hash(article ))

        request = urllib.request.Request(url)
        content = urllib.request.urlopen(request)
        jsaved = content.read().decode("utf-8")
        saved = json.loads(jsaved,"utf-8")

        return saved

    def __register(self, article):
        json_data = json.dumps(article).encode()
        request = urllib.request.Request(self.url, data=json_data)

        try:
            content = urllib.request.urlopen(request)
            return True
        except urllib.error.URLError:
            return False

    def save(self, article):
        article_prepared = self.__prepare(article)
        self.logging.debug("Saving...")

        #if not self.__feed_exists(article_prepared):
        self.__register(article_prepared)
        self.logging.debug("Done")
