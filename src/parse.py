"""
Class for the web crawling and parsing of the data
"""
from typing import List
from multiprocessing import Pool

class WebCrawling:
    def __init__(self, urls: List[str], tags: List[str]):
        self.urls = urls
        self.tags = tags

    def getData(self):
        pool = Pool(processes=4)
        pool.map(self.getWebData, self.urls)

    def getWebData(self, url):
        print(url)
