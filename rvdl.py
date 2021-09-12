#!/usr/bin/env python
from strategies import StreamableDownloadStrategy
from controllers import RedditController
from exceptions import InvalidQueryException

hostDownloadTable = {
    "streamable.com": StreamableDownloadStrategy("videos"),
    "streamwo.com": None
}

def start():
    print("Starting RVDL...")

    rc = RedditController()

    try:
        # data = use_subreddit(rc, "r/formula1", "hot", 50)
        data = use_post(rc, "https://www.reddit.com/r/formula1/comments/pmuxvu/george_russell_noticing_daniel_riccardo/")

        for datum in data:
            download(datum)

    except InvalidQueryException as e:
        print(e)

    except Exception as e:
        print(e)

def use_post(rc, post):
    listings = rc.process_post(post)

    if len(listings) < 1:
        return

    children = listings[0]["data"]["children"]  # Assert first listing holds post data, subsequent listings are comments in the thread.

    if len(children) == 1:
        data = children[0]["data"]  # Assert there is only one child returned from api when querying a single post.

        if data is None:    # No post available
            return
        else: 
            return [ data ]
    
    else:
        return

def use_subreddit(rc, subreddit, filter, limit):
        output = []

        listing = rc.process_subreddit(subreddit, filter, limit)
        children = listing["data"]["children"]

        if len(children) > 0:
            for child in children:
                data = child["data"]

                if data is None:    # No post available
                    continue
                else:
                    output.append(data)
        else:
            return

        return output

def download(data):
        if data is None:    # No post available
            return

        strategy = hostDownloadTable.get(data["domain"])

        if strategy is None:    # Host is not supported for download
            return
        
        file_name = strategy.download(data["url"])
        print(f"file name: {file_name}")

if __name__ == "__main__":
    start()