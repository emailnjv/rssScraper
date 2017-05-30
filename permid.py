import json
import requests


class Permid(object):
    url = "https://api.thomsonreuters.com/permid/calais"
    headers = {'X-AG-Access-Token': "sekrwZ0vvmGKVxl6nbZhocnfTyJomv6Z",
               'outputformat': 'application/json',
               'Content-Type': 'text/plain',
               'cache-control': "no-cache"
               }

    def __init__(self, logging):
        self.logging = logging

    def __request(self, value):
        url = self.url

        response = requests.request("POST", url, data=value.encode("utf-8"), headers=self.headers)


        return json.loads(response.text)

    def tag(self, word):
        self.logging.debug("accessing permid to " + word)
        content = self.__request(word.strip())
        topics = []
        tags = []

        for key, value in content.items():
            if "forenduserdisplay" in value.keys():
                if value["_typeGroup"] == "topics":
                    topics.append(value["name"])
                else:
                    if value["_typeGroup"] == "socialTag":
                        tags.append(value["name"])

        self.logging.debug("topics: " + ", ".join(topics))
        self.logging.debug("tags: " + ", ".join(tags))
        return {"topics": topics, "tags": tags}
