from constants import NAVER_URL, NAVER_SELECTOR
from web import Web
from urllib.parse import quote
from typing import List

class Naver(Web):
  def __init__(self):
    super().__init__()
    self._url = NAVER_URL
    self._selector = NAVER_SELECTOR
    self._date = ''
    self._keyword = ''

  def __get_data_page__(self, page_num: int):
    url = self.__get_url_with_option__(self._keyword, self._date, page_num)
    soup = self.get_request(url)
    if soup:
      return soup.select(self._selector)
    return None

  def get_data_day(self, keyword: str, date: str) -> List[str]:
    links = []
    self._date = date
    self._keyword = keyword
    page_max = 400
    return links

  def get_data(self, keyword: str, start_date: str, days: int) -> List[str]:
    links = []
    return links
