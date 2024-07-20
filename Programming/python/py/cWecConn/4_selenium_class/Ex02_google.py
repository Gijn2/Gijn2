'''
1. 크롬웹드라이버로 구글 사이트 열기

2. 실제 크롬창에서 '파이썬'라고 검색버튼을 누른다.
    개발자모드(F12)에서 이 부분을 보면
    <input name='q' value='파이썬'~~ >
    그리고 'google검색' 버튼이 type='submit' 인거 확인
'''

from selenium import webdriver
from selenium.webdriver.common.by import By # By만 쓸 수 있게끔 설정해주는 방법(간소화 해주는 작업)
from selenium.webdriver.chrome.options import  Options
from selenium.webdriver.chrome.service import  Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. webdriver 객체생성
options = Options()
"""
- 옵션에 추가


"""
options.add_experimental_option("detach",True)

service = Service(ChromeDriverManager().install()) # 크롬 드라이버매니저를 자체적으로 설치함
driver = webdriver.Chrome(options=options)        # 리소스를 다 받아오면 시작.

# 2. 페이지 접근
driver.get('https://www.google.com')
driver.implicitly_wait(2)                         # 크롬에서 자원을 다 로드 할때까지 직접 (2)초 기다림.

search_engine = driver.find_element(by=By.NAME,value='q')             # 크롬 검색엔진의 name을 찾아서 변수에 지정
search_engine.send_keys("서강대 냉면")
driver.find_element(by=By.NAME,value='btnK').click()



# 3. 화면을 캡처해서 저장하기
# driver.save_screenshot("Mysite.png") # 자기가 알아서 네이버를 띄우고 해당 창을 캡처한듯?
driver.save_screenshot("./img/Mysite.png")
