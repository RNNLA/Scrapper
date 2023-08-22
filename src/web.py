from bs4 import BeautifulSoup
from constants import HEADER
import requests
import time

class MaxRetry(Exception):
  def __init__(self, msg):
    self.msg = msg

  def __str__(self):
    return self.msg

class Web():
  def __init__(self):
    self._header = HEADER

  def get_request(self, url : str) -> (int, BeautifulSoup):
    soup = None
    tries = 0
    while tries < 3:
      try:
        time.sleep(5)
        response = requests.get(url, headers=self._header, timeout=10)
        status_code = response.status_code
        if status_code == 200:
          soup = BeautifulSoup(response.text, 'html.parser')
          return 200, soup
        print(f'Got http error: {status_code}')
      except requests.exceptions.Timeout as errd:
        print('Timeout Error : ', errd)
      except requests.exceptions.ConnectionError as errc:
        print('Error Connecting : ', errc)
      except requests.exceptions.HTTPError as errb:
        print('Http Error : ', errb)
      except requests.exceptions.RequestException as erra:
        print('AnyException : ', erra)
      finally:
        tries += 1
    raise MaxRetry(f'Failed to get page with {tries} tries: {status_code}')
