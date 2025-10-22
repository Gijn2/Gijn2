"""
    bs4 라이브러리 : 웹에서 가져온 HTML코드를 파이썬에서 사용하기 편하게 파싱해주는 라이브러리
            [참고] 웹에서 가져온 HTML코드 가져오는 방법
                - requests 모듈
                - urllib 의 request 모듈

    BeautifulSoup 모듈
        - find()
        - find_all()
    
    [참고] 파서의 종류 
        - lxml : c로 만들어져 속도 빠름
        - html5lib : 파이썬으로 만들어서 lxml보다 느림
        - html.parser (*): 파이썬 버전을 확인해서 사용
            ㄴ 구조 내 에서 필요한 부분을 찾기 위해 토막내서 가져오는 기능
"""

from bs4 import BeautifulSoup   # 뷰티풀soup가져오기

html = """
    <html>
        <body>
            <h1>스크레이핑 연습</h1>
            <p>웹페이지 분석하자</p>
            <p>데이타 정제하기</p>
        </body>
    </html>
"""

# 1. 데이타 파서하기
soup = BeautifulSoup(html,'html.parser')

# 2. 원하는 요소 접근하기
h1 = soup.html.body.h1  # 변수를 찾아서 h1 변수에 지정
print(h1)               # h1 태그까지 출력
print(h1.text)          # 태그 내의 문자만 출력 1
print(h1.string)        # 태그 내의 문자만 출력 2

print('='*100)

# 3. 요소의 내용 추출하기
# p = soup.html.body.p # 현실에서 홈페이지는 내용이 너~무 많다.
p = soup.find('p')
print(p)
print('-'*10)
p = soup.findAll('p')    # 리스트 형태로 출력
print(p)
print('-'*10)
p = soup.find_all('p')   # 리스트 형태로 출력
print(p)
print('-'*10)

# 데이터 요소 추출하기
for i in range (len(p)):
    print(f'{i+1} 번 데이터 추출하기 : {p[i]}')

