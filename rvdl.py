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
        listing = rc.process_subreddit("formula1", "hot", 100)

        children = listing["data"]["children"]

        if len(children) > 0:

            for child in children:
                data = child["data"]

                if data is None:    # No post available
                    continue

                strategy = hostDownloadTable.get(data["domain"])

                if strategy is None:    # Host is not supported for download
                    continue
                
                try:
                    file_name = strategy.download(data["url"])
                    print(f"file name: {file_name}")
                except Exception as e:
                    print(e)
            
        else:
            print("No posts found in subreddit.")

    except InvalidQueryException as e:
        print(e)

if __name__ == "__main__":
    start()