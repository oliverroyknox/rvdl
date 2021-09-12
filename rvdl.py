#!/usr/bin/env python
from controllers import RedditController
from exceptions import InvalidQueryException

def start():
    rc = RedditController()

    try:
        json = rc.process_subreddit("formula1", "hot", 10)
        print(json)
    except InvalidQueryException as e:
        print(e)

if __name__ == "__main__":
    start()