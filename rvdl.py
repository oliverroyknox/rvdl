#!/usr/bin/env python
from strategies import StreamableDownloadStrategy
from controllers import RedditController
from exceptions import InvalidQueryException

import argparse

def start():
    try:
        parser = argparse.ArgumentParser(description="Download videos from Reddit.")
        subparsers = parser.add_subparsers(dest="command")

        # download a video
        get = subparsers.add_parser("get")
        get.add_argument("url", metavar="U", type=str, help="The url of the post to download video from.")
        get.add_argument("--output", "-o", type=str, default="./", help="The output directory of the video.")
        
        # download videos in subreddit
        gets = subparsers.add_parser("gets")
        gets.add_argument("name", metavar="S", type=str, help="The subreddit to download video(s) from.")
        gets.add_argument("--filter", "-f", type=str, default="hot", help="The filtering option for a subreddit.")
        gets.add_argument("--output", "-o", type=str, default="./", help="The output directory of the video(s).")

        args = parser.parse_args()

        rc = RedditController()
        data = []

        if args.command == "get":
            data = use_post(rc, args.url)
        elif args.command == "gets":
            data = use_subreddit(rc, args.name, args.filter, 100)
    
        hostDownloadTable = {
            "streamable.com": StreamableDownloadStrategy(args.output),
            "streamwo.com": None
        }

        for datum in data:
            download(datum, hostDownloadTable)

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

def download(data, hostDownloadTable):
        if data is None:    # No post available
            return

        strategy = hostDownloadTable.get(data["domain"])

        if strategy is None:    # Host is not supported for download
            return
        
        file_name = strategy.download(data["url"])
        print(f"file name: {file_name}")

if __name__ == "__main__":
    start()