from controllers.streamable import StreamableController
from uuid import uuid4

import re
import requests
import os.path

class StreamableDownloadStrategy():

    def __init__(self, path):
        self.controller = StreamableController()
        self.path = path
        self.invalid_chars_rx = re.compile(r"[\\/:\"*?<>|]+")

    def download(self, url):
        video = self.controller.process_clip(url)

        files = video["files"]

        if files is None:
            raise AttributeError("streamable controller returned a null value for files.")

        file = files["mp4"] or files["mov"] or files["avi"]
        url = file["url"]

        if url is None:
            raise AttributeError("streamable controller return a null value for url.")

        file_name = re.sub(self.invalid_chars_rx, "", f"{video['title']} {uuid4()}.mp4")
        
        response = requests.get(url, stream=True, headers={ "User-Agent": "rvdl" })
        
        path = os.path.join(self.path, file_name)

        with open(path, "wb") as file:
            for chunk in response.iter_content(chunk_size=2048):
                if chunk:
                    file.write(chunk)

        return file_name