from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import datetime as dt
import time
from typing import List
from typing import Optional

class link_getter :
    # selectors per site to get links. Choose one where you want to get links.
    site = {
        'naver' : {
            'url' : "https://search.naver.com/search.naver?where=news&query=",
            'selector' : "#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div.info_group > a.info"
        }
    }

    def __init__(self, excel_name = "risk_dictionary.xlsx"):
        self.data_src = pd.read_excel(excel_name, sheet_name="1. 반도체 공급망 RISK 키워드 POOL")
        self.total_cnt = 0

    def get_link_by_naver(self, 
                          file_name : str, 
                          data : Optional[List[str]] = None, 
                          url : Optional[str] = None,
                          selector : Optional[str] = None,
                          start_date : Optional[dt.date] = None,
                          end_date : Optional[dt.date] = None,
                          repeat  : Optional[int] = None):
        _json = []
        self.total_cnt = 0
        _repeat = 400 if repeat is None else repeat if repeat <= 400 else 400
        _data = self.data_src if data is None else data
        _cur_date = start_date if start_date is not None else dt.date.today()
        _end_date = end_date if dt.date(_end_date.year, _end_date.month-1, _end_date.day-1) is not None else dt.date(_cur_date.year, _cur_date.month-1, _cur_date.day-1)
        base_url = url if url is not None else link_getter.site.get('naver').get('url')
        _selector = selector if selector is not None else link_getter.site.get('naver').get('selector')
        
        for key in _data:
            print(f"{key} started") #print log. Erase it if you don't want any log
            _json = self._get_dict(_json, base_url, key, _cur_date, _end_date, _repeat, _selector)
            print(f"{key} ended") #print log. Erase it if you don't want any log
                
        self._to_json(file_name = file_name, json_file = _json)
    

    def _get_dict(self, json, base_url, key, _cur_date, _end_date, _repeat, _selector) :
        _json = json
        while(_cur_date != _end_date) :
                prev_date = _cur_date - dt.timedelta(days = 1)
                for page_num in range(_repeat):
                    cur_url =  self._get_url(base_url, key, page_num, '&sort=1', '&pd=3', f'&ds={_cur_date.strftime("%Y.%m.%d")}', f'&de={_cur_date.strftime("%Y.%m.%d")}')
                    try : # Need exception handling improvement. 
                        html = requests.get(cur_url)
                        soup = BeautifulSoup(html.text, 'html.parser')
                    except Exception as ex:
                        print('error during html request & parsing')
                        print(ex)
                        return None
                    print(cur_url) #print log. Erase it if you don't want any log

                    _json = self._get_page_data(soup, _selector, _json)
                    time.sleep(0.5)
                _cur_date = prev_date
        return _json
    
    def _get_page_data(self, soup, selector, json) :
         # Need exception handling improvement : If No data in page.
        for elem in soup.select(selector):
                if(len(elem['class']) > 1) :
                    continue
                self.total_cnt += 1
                link = elem['href']
                dictionary = {f'{self.total_cnt}' : link}
                json.append(dictionary)
        return json

    
    def _get_url(self, url : str, key : str, page_num : int, *args : str) :
        params = ''
        for idx, arg in enumerate(args):
            params += arg
        return url + key + "&start=" + str(page_num * 10 + 1) + params
    

    def _to_json(self, file_name : str, json_file : List[str]) :
         # Need exception handling improvement
        with open(file_name, 'w') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)
            



lg = link_getter()
lg.get_link_by_naver('naver.json', ['반도체'], end_date = dt.date(2023,8,13))
