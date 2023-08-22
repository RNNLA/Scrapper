from typing import List
from web import Web, MaxRetry
import re

class Article(Web):
  def __init__(self):
    super().__init__()
    self._regex_formats = (r'[\\\t\\\r\\\n]',)

  def __get_cleaned_data__(self, data: List[str]) -> List[str]:
    return [self.__clean_text__(line.text) for line in data]

  def __clean_text__(self, text: str) -> str:
    copied_text = text
    for regex in self._regex_formats:
      copied_text = re.sub(regex, '', copied_text)
    return copied_text

  def get_text_url(self, url: str, tags: List[str]) -> List[str] | None:
    data = []
    try:
      if len(tags) != 3:
        raise ValueError('The number of tags must be 3')
      status_code, soup = self.get_request(url)
      if status_code == 200:
        data += [self.__get_cleaned_data__(soup.select(tag)) for tag in tags]
      return data
    except MaxRetry as mr:
      print(mr)
    except ValueError as ve:
      print('Value Error : ', ve)
    return None