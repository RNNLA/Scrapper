from typing import List
from bs4 import BeautifulSoup
import chardet
import requests
import re
from enum import Enum

class ParseType(Enum):
    SINGLE = 1
    MULTI = 2

class WebCrawling:
    def __init__(self, urls: List[str], tags: List[str]):
        self.regex_formats = (
            r'[\\\t\\\r\\\n]',
        ) 
        self._urls = urls
        self._tags = tags
        self._header = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
        self._data = list()

    def run(self) -> List | None:
        try:
            if len(self._tags) != 3:
                raise Exception('The number of tags must be 3')
            self._runEach()
            return self._data
        except Exception as e:
            print(e)
            return None

    def _runEach(self) -> None:
        data = list()
        for url in self._urls:
            cleaned_data = self._getData(url)
            data.append(cleaned_data)
        self._data = data

    def _getData(self, url: str) -> List | None:
        data = list()
        try:
            response = requests.get(url, headers=self._header)
            if response.status_code != 200:
                raise Exception('The status code is not 200')
            soup = BeautifulSoup(response.text, 'html.parser')
            title, content, date = self._tags
            data.append(self._extractData(soup, title, ParseType.SINGLE))
            data.append(self._extractData(soup, content, ParseType.MULTI))
            data.append(self._extractData(soup, date, ParseType.SINGLE))
            return data
        except Exception as e:
            print('Error occured while getting data\n{0}'.format(e))
            return None

    def _extractData(self, soup: BeautifulSoup, tag: str, parse_type: ParseType) -> str:
        if parse_type == ParseType.SINGLE:
            return self._cleanText(soup.select_one(tag).text)
        elif parse_type == ParseType.MULTI:
            return [self._cleanText(selected_el.text) for selected_el in soup.select(tag)]
        else:
            return None

    def _cleanText(self, text: str) -> str:
        _text = text
        for regex in self.regex_formats:
            _text = re.sub(regex, '', _text)
        return _text
