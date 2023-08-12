from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import json

class link_getter :
    def __init__(self, excel_name = "risk_dictionary.xlsx", base_url = "https://search.naver.com/search.naver?where=news&query="):
        self.data_src = pd.read_excel(excel_name, sheet_name="1. 반도체 공급망 RISK 키워드 POOL")
        self.base_url = base_url

        # self.data_col_list = ['주요 업체', '주요 원자재', '파운드리 기업', '반도체 기업', '기타 관련 기업', '반도체 소재 업체', '반도체 웨이퍼 업체', '반도체 장비 업체', '기구 및 협회', '반도체 공통용어', '반도체 기술 용어', '반도체 생태계 용어', '반도체 공정 용어', '반도체 소재']
        self.data_col_list = ['반도체 공통용어']

    # flag = 0 : Use all keywords from excel files. You can designate columns, if you don't want all columns.
    # flag = 1 : Use your own data set. Use it if you want one or two words instead of whole things.
    def get_link_by_naver(self, data = [], flag = 0, columns = []):
        _json = []
        total_cnt = 0
        
        data = {
            0 : self._get_data_by_col(columns),
            1 : data
        }.get(flag)

        for key in data:
            print(f"{key} started") #print log. Erase it if you don't want any log

            for page_num in range(10):
                url = self.base_url + key + self._add_param(page_num, '&sort=1')
                html = requests.get(url)
                soup = BeautifulSoup(html.text, 'html.parser')
                print(url) #print log. Erase it if you don't want any log
            
                for elem in soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > a'):
                    if(len(elem['class']) > 1) :
                        continue
                    total_cnt += 1
                    link = elem['href']
                    dictionary = {f'{total_cnt}' : link}
                    _json.append(dictionary)

            print(f"{key} ended") #print log. Erase it if you don't want any log
            time.sleep(0.5)

        self._to_json(file_name = 'naver_test.json', json_file = _json)

    def _get_data_by_col(self, columns = []):
        if len(columns) == 0 :
            columns = self.data_col_list

        data = []

        for col in columns:
            data += self.data_src[col].dropna(axis = 0).tolist()

        return data
    

    def _add_param(self, page_num, *args) :
        _ = ''
        for idx, arg in enumerate(args):
            _ += arg
        return "&start=" + str(page_num * 10 + 1) + _
    

    def _to_json(self, file_name, json_file) :
        with open(file_name, 'w') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)
            
            

lg = link_getter()
lg.get_link_by_naver()