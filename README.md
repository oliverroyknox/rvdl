# Reddit Video Downloader

## Description

RVDL is a command line tool to download videos from Reddit. It interfaces with the Reddit API to locate where the video is hosted and selects a strategy for the hosting service, if it is supported. Single or batch operations are available (see [Usage](#usage)).

## Usage

|Command|Description| 
|---|---|
|```rvdl get <url>```|Downloads a single video from the specified url into the current directory.
|```rvdl get -o <directory>```|Downloads a single video from the specified url into the output directory.
|```rvdl gets <subreddit>```|Downloads multiple videos, filtered by hot, of the given subreddit into the current directory.
|```rvdl gets <subreddit> -f <filter>```|Downloads multiple videos, using the specified filter, of the given subreddit into the current directory.
|```rvdl gets <subreddit> -o <directory>```|Downloads multiple videos, filtered by hot, of the given subreddit into the output directory.
||

<b>Example</b>

To download single video into an output directory.

```bash
rvdl get "reddit.com/r/<subreddit>/comments/<shortcode>/<postname>" -o "videos/reddit"
```

To download the top 100 videos in a subreddit.

```bash
rvdl gets "<subreddit>" -f "top" -o "videos/reddit/top" 
```

*To comply with the [Reddit's API access rules](https://github.com/reddit-archive/reddit/wiki/API) a limit of 100 posts is enforced when querying a subreddit's posts.

## Installation

## Contribution