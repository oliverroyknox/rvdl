import re
import requests
from exceptions import InvalidQueryException

class RedditController():

    def __init__(self):
        self.filter_rx = re.compile(r"^(hot|new|top|controversial|rising)$")
        self.subreddit_rx = re.compile(r"^[A-Za-z0-9]+(?:[_-][A-Za-z0-9]+)*$")

    def process_subreddit(self, subreddit, filter, limit):
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

        return response.json()



