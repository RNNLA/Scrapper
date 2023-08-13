from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time
from typing import List
from typing import Tuple

class link_getter :
    full_columns : List[str] = ['주요 업체', '주요 원자재', '파운드리 기업', '반도체 기업', '기타 관련 기업', '반도체 소재 업체', '반도체 웨이퍼 업체', '반도체 장비 업체', '기구 및 협회', '반도체 공통용어', '반도체 기술 용어', '반도체 생태계 용어', '반도체 공정 용어', '반도체 소재']
    
    def __init__(self, excel_name = "risk_dictionary.xlsx", base_url = "https://search.naver.com/search.naver?where=news&query="):
        self.data_src = pd.read_excel(excel_name, sheet_name="1. 반도체 공급망 RISK 키워드 POOL")
        self.base_url = base_url

    # flag = False : Use all keywords from excel files. You can designate columns, if you don't want all columns.
    # flag = True : Use your own data set. Use it if you want one or two words instead of whole things.
    def get_link_by_naver(self, file_name : str, flag : bool, data : List[str] = [], columns : List[str] = [], repeat  : int = 5):
        _json = []
        total_cnt = 0
        try:            
            _data = self._get_data_by_col(columns) if flag == False else data
            if (flag == True) and (len(data) == 0):
                raise Exception('You must enter the data, not the empty list')

        except Exception as ex:
            print(ex)
            return None
        
        for key in _data:
            print(f"{key} started") #print log. Erase it if you don't want any log

            for page_num in range(repeat):
                url = self.base_url + key + self._add_param(page_num, '&sort=1')
                html = requests.get(url)
                soup = BeautifulSoup(html.text, 'html.parser')
                print(url) #print log. Erase it if you don't want any log
            
                for elem in soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div.info_group > a.info'):
                    if(len(elem['class']) > 1) :
                        continue
                    total_cnt += 1
                    link = elem['href']
                    dictionary = {f'{total_cnt}' : link}
                    _json.append(dictionary)
                time.sleep(0.5)

            print(f"{key} ended") #print log. Erase it if you don't want any log
            
        self._to_json(file_name = file_name, json_file = _json)


    def _get_data_by_col(self, columns = []):
        if len(columns) == 0 :
            raise Exception('You don\'t enter any columns.')

        data = []

        for col in columns:
            data += self.data_src[col].dropna(axis = 0).tolist()
        return data
    

    def _add_param(self, page_num, *args) :
        params = ''
        for idx, arg in enumerate(args):
            params += arg
        return "&start=" + str(page_num * 10 + 1) + params
    

    def _to_json(self, file_name, json_file) :
        with open(file_name, 'w') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)
    


lg = link_getter()
lg.get_link_by_naver('naver_text.json', True)
lg.get_link_by_naver('naver_text.json', False)


