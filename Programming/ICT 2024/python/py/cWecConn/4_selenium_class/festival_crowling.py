import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select

# 1. webdriver 객체생성
options = Options()
options.add_experimental_option("detach",True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options)

# 2. page 접근
# -1. 접근 변수 설정
url = 'https://korean.visitkorea.or.kr/kfes/list/wntyFstvlList.do'
site = requests.get(url)

# -2. page 연결
driver.get(url)
driver.implicitly_wait(1) # 화면 구동 후 대기

# 3. 검색 엔진에 원하는 값 입력 및 검색버튼 클릭
search_engine = driver.find_element(by=By.NAME, value='searchArea')
Select(search_engine).select_by_value("1")
search_engine.click()

driver.find_element(by=By.CLASS_NAME, value='btn_search').click()
time.sleep(1)
# 4. 서울시에 관련된 정보만 크롤링할 준비.
find_ul = driver.find_element(by=By.CLASS_NAME, value='other_festival_ul')

data = []

print(find_ul.text)

time.sleep(5)
driver.close()
