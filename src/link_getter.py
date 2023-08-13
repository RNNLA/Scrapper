from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

import time
from typing import List




class link_getter :
    # all columns from the excel file. Use it if you want full columns or default value.
    full_columns = ['주요 업체', '주요 원자재', '파운드리 기업', '반도체 기업', '기타 관련 기업', '반도체 소재 업체', '반도체 웨이퍼 업체', '반도체 장비 업체', '기구 및 협회', '반도체 공통용어', '반도체 기술 용어', '반도체 생태계 용어', '반도체 공정 용어', '반도체 소재']
    # selectors per site to get links. Choose one where you want to get links.
    link_selector = {
        'naver' : '#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div.info_group > a.info',
    }

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
                url = self.base_url + key + self._add_param(page_num, '&sort=1', '&pd=5')

                try :
                    html = requests.get(url)
                except Exception as ex:
                    print('error from the request side')
                    print(ex)
                    return None
                
                try :
                    soup = BeautifulSoup(html.text, 'html.parser')
                except Exception as ex:
                    print('error from the bs side')
                    print(ex)
                    return None
                
                print(url) #print log. Erase it if you don't want any log
            
                for elem in soup.select(link_getter.link_selector.get('naver')):
                    if(len(elem['class']) > 1) :
                        continue

                    total_cnt += 1
                    link = elem['href']
                    dictionary = {f'{total_cnt}' : link}
                    _json.append(dictionary)

                time.sleep(0.5)

            print(f"{key} ended") #print log. Erase it if you don't want any log
            
        self._to_json(file_name = file_name, json_file = _json)


    def _get_data_by_col(self, columns : List[str]):
        if len(columns) == 0 :
            raise Exception('You don\'t enter any columns.')

        data = []

        for col in columns:
            data += self.data_src[col].dropna(axis = 0).tolist()
        return data
    

    def _add_param(self, page_num : int, *args : str) :
        params = ''
        for idx, arg in enumerate(args):
            params += arg
        return "&start=" + str(page_num * 10 + 1) + params
    

    def _to_json(self, file_name : str, json_file : List[str]) :
        with open(file_name, 'w') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)


    


lg = link_getter()
lg.get_link_by_naver('naver_text.json', flag = False, columns = link_getter.full_columns, repeat = 1)


