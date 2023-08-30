from .constants import URL, SELECTOR, DATA_PATH
from .web import Web
from .exceptions import MaxRetry, NoDataException
from urllib.parse import quote
from typing import List
from dateutil.parser import parse
import datetime as dt
import pandas as pd

def string_to_date(date: str, date_format: str) -> None:
  return parse(date).strftime(date_format)

def write_to_csv(data: List[str], keyword: str, date: str) -> None:
  date = string_to_date(date, '%Y-%m-%d')
  data_frame = pd.DataFrame(data, columns = ['links'])
  file = f'{DATA_PATH}{date}_{keyword}.csv'
  data_frame.to_csv(file, sep = ',', index = False)

class Scrapper(Web):
  def __init__(self):
    super().__init__()
    self._url = URL
    self._selector = SELECTOR
    self._date = None
    self._keyword = None
    self.page_max = 400

  def __get_url__(self, page_num: int) -> str:
    if page_num is None:
      raise ValueError(f'page_num is negative: {page_num}')
    date = string_to_date(self._date, '%Y.%m.%d')
    query = f'&start={page_num * 10 + 1}&sort=1&pd=3&ds={date}&de={date}'
    return f'{self._url}{quote(self._keyword)}{query}'

  def __get_link_from_page__(self, data: List[str]) -> List[str]:
    if len(data) == 0:
      raise NoDataException(f'Finished for {self._keyword} {self._date}')
    return [link['href'] for link in data if 'press' not in link['class']]

  def __get_data_page__(self, page_num: int) -> List[str]:
    url = self.__get_url__(page_num)
    print(f'Searching in {self._keyword} {self._date} page {page_num + 1}')
    status_code, soup = self.get_request(url)
    if status_code == 200:
      return self.__get_link_from_page__(soup.select(self._selector))

  def get_data_day(self, keyword: str, date: str) -> None:
    links = []
    self._date = date
    self._keyword = keyword
    try:
      if self._keyword is None or self._date is None:
        raise TypeError('keyword or date got none')
      for page in range(self.page_max):
        links += self.__get_data_page__(page)
    except ValueError as ve:
      print(ve)
    except TypeError as te:
      print(te)
    except MaxRetry as mr:
      print(mr)
    except NoDataException as ne:
      print(ne)
    write_to_csv(links, self._keyword, self._date)

  def get_data(self, keyword: str, start_date: str, days: int) -> None:
    start = parse(start_date)
    date_list = [start - dt.timedelta(days=x) for x in range(days)]
    for date in date_list:
      self.get_data_day(keyword, date.strftime('%Y.%m.%d'))
