from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime
import random
import pandas as pd
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())

def scroll():
    try:        
        # 페이지 내 스크롤 높이 받아오기
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            # 임의의 페이지 로딩 시간 설정
            # PC환경에 따라 로딩시간 최적화를 통해 scraping 시간 단축 가능
            pause_time = random.uniform(1, 2)
            # 페이지 최하단까지 스크롤
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            # 페이지 로딩 대기
            time.sleep(pause_time)
            # 무한 스크롤 동작을 위해 살짝 위로 스크롤(i.e., 페이지를 위로 올렸다가 내리는 제스쳐)
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
            time.sleep(pause_time)
            # 페이지 내 스크롤 높이 새롭게 받아오기
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            
            # 스크롤을 완료한 경우(더이상 페이지 높이 변화가 없는 경우)
            if new_page_height == last_page_height:
                print("스크롤 완료")
                break
                
            # 스크롤 완료하지 않은 경우, 최하단까지 스크롤
            else:
                last_page_height = new_page_height
            
    except Exception as e:
        print("에러 발생: ", e)

driver = webdriver.Chrome(service=service)

# 스크래핑 할 URL 세팅
URL = "https://www.youtube.com/playlist?list=PLCS0nOWWS-Pn_uKoBRdktvIqcXNZ_G3w_"
# 크롬 드라이버를 통해 지정한 URL의 웹 페이지 오픈
driver.get(URL)
# 웹 페이지 로딩 대기
time.sleep(3)
# 무한 스크롤 함수 실행
scroll()

# 페이지 소스 추출
html_source = driver.page_source
soup_source = BeautifulSoup(html_source, 'html.parser')

# 콘텐츠 모든 정보
content_total = soup_source.find_all('a','yt-simple-endpoint style-scope ytd-playlist-video-renderer')
# 썸네일 불러오기
# content_thum = soup_source.find_all('img','yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded')

# 콘텐츠 제목만 추출
content_title = list(map(lambda data: data.get_text().replace("\n", "").strip().replace("[PUMP IT UP XX]", "").strip().replace("[펌프잇업 20주년]", "").strip(), content_total))
# 콘텐츠 링크만 추출
content_link = list(map(lambda data: data["href"].replace("/watch?v=", "").strip()[0:11], content_total))

#썸네일 주소 추출
# content_img = list(map(lambda data: data["src"], content_thum))

# 딕셔너리 포맷팅
content_total_dict = {'title':content_title, 
                      'url':content_link,
                      'level':'27',
                     }

data_save = pd.DataFrame(content_total_dict)
#데이터를 저장 
data_save.to_csv("27-2.csv", encoding='utf-8-sig')
