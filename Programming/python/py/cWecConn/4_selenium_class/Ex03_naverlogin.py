"""
네이버 로그인 페이지를 실행하기
    크롬에서 네이버 로그인 페이지를 개발자모드에서 확인하여
    로그인 폼의 아이디와 비밀번호 입력 name 확인
    아이디 : id
    비밀번호 : pw
"""

from selenium import webdriver

# 0. 네이버 로그인 정보 -> 안됨 -> atosoft
myID = '한기진'
myPW = '6439'

from selenium.webdriver.common.by import By # By만 쓸 수 있게끔 설정해주는 방법(간소화 해주는 작업)
from selenium.webdriver.chrome.options import  Options
from selenium.webdriver.chrome.service import  Service
from webdriver_manager.chrome import ChromeDriverManager


# 1. webdriver 객체생성
options = Options()
"""
- 옵션에 추가
"""
options.add_experimental_option("detach",True)

serice = Service(ChromeDriverManager().install()) # 크롬 드라이버매니저를 자체적으로 설치함
driver = webdriver.Chrome(options=options)        # 리소스를 다 받아오면 시작.

# 2. 페이지 접근
driver.get('http://ictedu.atosoft.net/worknet/SLogin.asp')
driver.implicitly_wait(2)                         # 크롬에서 자원을 다 로드 할때까지 직접 (2)초 기다림.

# 3.
# atosoft
driver.find_element(By.NAME,'strSName').send_keys(myID)         # 이름에 해당하는 녀석에게 아이디 주기
driver.implicitly_wait(2)                                             # 이름에 해당하는 정보가 나올 때까지 기다리기
driver.find_element(By.ID,'ui-id-1').click()                    # 정보 리스트가 나오면 해당하는 이름 클릭
driver.find_element(By.NAME,'strLoginPwd').send_keys(myPW)      # 비밀번호 입력
driver.find_element(By.CLASS_NAME,'btn-info').click()           # 로그인