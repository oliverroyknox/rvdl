from exceptions import InvalidQueryException

import re
import requests

class StreamableController():

    def __init__(self):
        self.shortcode_rx = re.compile(r"[\/\w*\d*]{6}$")   # assumes shortcode is an alphanumeric string with a length of 6

    def process_clip(self, url):
        shortcode = re.search(self.shortcode_rx, url).group(0)

        if shortcode is None:
            raise InvalidQueryException("no valid shortcode detected in supplied url.")
        
        response = requests.get(
            url=f"https://api.streamable.com/videos/{shortcode}",
            headers={ "User-Agent": "rvdl", "Content-Type": "application/json" }
        )

        if not response.ok:
            raise InvalidQueryException(f"request failed with error code {response.status_code}; the reason is {response.reason}.")

        return response.json()