from typing import List
from bs4 import BeautifulSoup
import requests
import re
from enum import Enum

class ExtractType(Enum):
  SINGLE = 1
  MULTI = 2

class WebCrawling:
  def __init__(self, urls: List[str], tags: List[str]):
    self._regex_formats = (r'[\\\t\\\r\\\n]',)
    self._urls = urls
    self._tags = tags
    self._header = ({'User-Agent':
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
      (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
      'Accept-Language': 'en-US, en;q=0.5'})
    self._data = []

  def run(self) -> List | None:
    try:
      if len(self._tags) != 3:
        raise ValueError('The number of tags must be 3')
      self._run_each()
      return self._data
    except ValueError as ve:
      print('Value Error : ', ve)
      return None
    except requests.exceptions.Timeout as errd:
      print('Timeout Error : ', errd)
    except requests.exceptions.ConnectionError as errc:
      print('Error Connecting : ', errc)
    except requests.exceptions.HTTPError as errb:
      print('Http Error : ', errb)
    except requests.exceptions.RequestException as erra:
      print('AnyException : ', erra)

  def _run_each(self) -> None:
    data = []
    for url in self._urls:
      cleaned_data = self._get_data(url)
      data.append(cleaned_data)
    self._data = data

  def _get_data(self, url: str) -> List | None:
    data = []
    response = requests.get(url, headers=self._header, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    title, content, date = self._tags
    data.append(self._extract_data(soup, title, ExtractType.SINGLE))
    data.append(self._extract_data(soup, content, ExtractType.MULTI))
    data.append(self._extract_data(soup, date, ExtractType.SINGLE))
    return data

  def _extract_data(self,
                    soup: BeautifulSoup,
                    tag: str, extract_type: ExtractType) -> str | None:
    if extract_type == ExtractType.SINGLE:
      return self._clean_text(soup.select_one(tag).text)
    elif extract_type == ExtractType.MULTI:
      return [self._clean_text(selected.text) for selected in soup.select(tag)]
    return None

  def _clean_text(self, text: str) -> str:
    copied_text = text
    for regex in self._regex_formats:
      copied_text = re.sub(regex, '', copied_text)
    return copied_text
