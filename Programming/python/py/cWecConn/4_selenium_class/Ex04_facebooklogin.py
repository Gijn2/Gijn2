"""
    [연습] 페이스북에 접속해서 로그인 하기

        로그인 후에 보안창은 없는데 안 넘어가서

        from selenium.webdriver.common.keys import Keys

        아이디와 패스워드 지정후에
        elem.send_keys(Keys.RETURN)

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
from selenium.webdriver.chrome.service import  Service
from webdriver_manager.chrome import ChromeDriverManager

myID = '33@gmail.com'
myPW = '33'

options = Options()
serice = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options)
# ==================================================================================
driver.get('https://github.com/login')
driver.implicitly_wait(2)

print("document.getElementByName('id')[0].value='{}'".format(myID))
driver.execute_script("document.getElementByName('id')[0].value='{}'".format(myID)) # JAVA Script 함수 호출하듯 안의 내용을 작성한다.
driver.execute_script("document.getElementByName('pw')[0].value='{}'".format(myPW))

driver.find_element(By.ID,value="log.login").click()