"""
    BeautifulSoup 모듈에서
    - HTML의 구조(=트리구조)에서 요소를 검색할 때 : find() / find_all()
    - CSS 선택자 검색할 때 : select() /  select_one()
"""

from bs4 import BeautifulSoup
from  urllib import  request as req

html = """
    <html><body>
        <div id='course'>
            <h1>빅데이터 과정</h1>
        </div>
        <div id='subjects'> 
            <ul class='subs'>
                <li>머신러닝</li>
                <li>데이터 처리</li>
                <li>데이타 분석</li>
            </ul>
        </div>
    </body></html>
"""

soup = BeautifulSoup(html,'html.parser')

# id값으로 찾기
h1 = soup.select('#course > h1') # select 요소가 여러 개이므로 리스트로 가져온 값을 출력해서 확인해보기
print(h1[0].text)                # 리스트형태
print('='*100)

# class명으로 찾기

h2 = soup.select('li')
for i in range(len(h2)):
    print(h2[i].text)
"""
for i in h2:
    print(i.text)
"""



