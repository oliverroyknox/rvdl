from exceptions.invalid_query import InvalidQueryException
from threading import Thread

class DownloadWorker(Thread):

    def __init__(self, queue, hs_table):
        Thread.__init__(self)
        self.queue = queue
        self.hs_table = hs_table

    def run(self):
        while True:            
            host, url = self.queue.get()

            try:
                self.__download(host, url)
            finally:
                self.queue.task_done()

    def __download(self, host, url):
        strategy = self.hs_table.get(host)

        if strategy is None:    # Host is not supported for download
            return
        
        try:
            file = strategy.download(url)
            print(f"downloaded: {file}")
        except InvalidQueryException as e:
            print(e)