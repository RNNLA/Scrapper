from bs4 import BeautifulSoup
from urllib.error import HTTPError
from constants import HEADER
import requests

class Web():
  def __init__(self):
    self._header = HEADER

  def get_request(self, url : str):
    soup = None
    try:
      response = requests.get(url, headers=self._header, timeout=10)
      response.raise_for_status()
      soup = BeautifulSoup(response.text, 'html.parser')
    except HTTPError as errb:
      print('Http Error : ', errb)
    return soup
