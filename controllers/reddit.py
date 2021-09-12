import re
import requests
from exceptions import InvalidQueryException

class RedditController():

    def __init__(self):
        self.filter_rx = re.compile(r"^(hot|new|top|controversial|rising)$")
        self.subreddit_rx = re.compile(r"^[A-Za-z0-9]+(?:[_-][A-Za-z0-9]+)*$")
        self.r_slash_rx = re.compile(r"^(r\/)")

    def process_post(self, post):
        response = requests.get(
            url=f"{post}.json", 
            headers={ "User-Agent": "rvdl", "Content-Type": "application/json" }
        )
        
        json = response.json()

        if not response.ok:
            raise InvalidQueryException(f"{json['message'] + ''.lower()}; request failed.")

        return json

    def process_subreddit(self, subreddit, filter, limit):
        subreddit = re.sub(self.r_slash_rx, "", subreddit) # common practice is to preceed a subreddit name with "r/", we remove this before validating to possibly accept this value. 

        if re.match(self.subreddit_rx, subreddit) is None:
            raise InvalidQueryException(f"{subreddit}; is not a valid subreddit name.")
        
        if re.match(self.filter_rx, filter) is None:
            raise InvalidQueryException(f"{filter}; is not a valid filtering option.")

        if limit < 1 or limit > 100:
            raise InvalidQueryException(f"{limit}; is out of the valid range of a queries limit, the value must be between 1 and 100.")

        response = requests.get(
            url=f"https://reddit.com/r/{subreddit}/{filter}.json",
            params={ "limit": limit },
            headers={ "User-Agent": "rvdl", "Content-Type": "application/json" }
        )

        json = response.json()

        if not response.ok:
            raise InvalidQueryException(f"{json['message'] + ''.lower()}; request failed.")

        return json
