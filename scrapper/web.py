from bs4 import BeautifulSoup
from .constants import HEADER, MAX_RETRY
from .exceptions import MaxRetry
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
import requests
import time
import random

class Web():
  def __init__(self):
    self._header = HEADER
    self._proxies = {
      'http': 'socks5://127.0.0.1:9050',
      'https': 'socks5://127.0.0.1:9050'
    }
    self._ip = None

  def __set_header__(self):
    self._header = {'User-Agent': UserAgent().random}

  def __get_ip__(self):
    response = requests.get('http://icanhazip.com/', proxies=self._proxies,
                            headers=self._header, timeout=10)
    return response.text.strip()

  def __set_ip__(self):
    new_ip = self.__get_ip__()
    while self._ip == new_ip:
      with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
      new_ip = self.__get_ip__()
    self._ip = new_ip
    print(f'IP changed to {self._ip}')

  def __get_request_internal__(self, url: str) -> (int, BeautifulSoup):
    status_code = 0
    soup = None
    tries = 0
    while tries < MAX_RETRY:
      try:
        time.sleep(random.randrange(3, 4))
        self.__set_header__()
        response = requests.get(url, proxies=self._proxies,
                                headers=self._header, timeout=10)
        status_code = response.status_code
        if status_code == 200:
          soup = BeautifulSoup(response.text, 'html.parser')
          return 200, soup
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
    return status_code, None

  def get_request(self, url : str) -> (int, BeautifulSoup):
    tries = 0
    status_code = 0
    self._ip = self.__get_ip__()
    print(f'IP start with {self._ip}')
    while tries < MAX_RETRY:
      status_code, soup = self.__get_request_internal__(url)
      if status_code == 200:
        return status_code, soup
      tries += 1
      self.__set_ip__()
    raise MaxRetry(f'Failed to get page with {tries} tries: {status_code}')
