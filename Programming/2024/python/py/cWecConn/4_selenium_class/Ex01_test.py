"""
 간단하게 크롬 브라우저를 실행하여 페이지 열기

 [4버전] import가 다양하다.
 진짜 ㅈㄴ 많음
"""
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

serice = Service(ChromeDriverManager().install()) # 크롬 드라이버매니저를 자체적으로 설치함
driver = webdriver.Chrome(options=options)        # 리소스를 다 받아오면 시작.

# 2. 페이지 접근
driver.get('https://www.daum.net')
driver.implicitly_wait(2)                         # 크롬에서 자원을 다 로드 할때까지 직접 (2)초 기다림.
