from bs4 import BeautifulSoup
import requests
import pandas as pd

class link_getter :
    def __init__(self):
        self.data = pd.read_excel("risk_dictionary.xlsx", sheet_name="1. 반도체 공급망 RISK 키워드 POOL")
        self.base_url = "https://search.naver.com/search.naver?where=news&query="
        self.sort = "&sort=1"
        # self.column_list = ['주요 업체', '주요 원자재', '파운드리 기업', '반도체 기업', '기타 관련 기업', '반도체 소재 업체', '반도체 웨이퍼 업체', '반도체 장비 업체', '기구 및 협회', '반도체 공통용어', '반도체 기술 용어', '반도체 생태계 용어', '반도체 공정 용어', '반도체 소재']
        self.column_list = ['반도체 공통용어']
#sp_nws1
    def get_link_by_naver(self):
        cnt = 0
        for column in self.column_list:
            cur_rows = self.data[column].dropna(axis = 0).tolist()
            # for key in cur_rows:
            # 나중에 다 탭으로 넣어
            key = cur_rows[0]
            url = self.base_url + key + self.sort + "&start=11"
            print(url)
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')

            # _ = [elem.select_one('.bx > a').get('href') for elem in soup.select('#main_pack > section > div > div.group_news > ul')]
            # for elem in soup.select('#main_pack > section > div > div.group_news > ul > li'):
            for elem in soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > a'):
                print(elem)
                print()
            
            

    
    # def search(self, key):
    #     pass

lg = link_getter()
lg.get_link_by_naver()