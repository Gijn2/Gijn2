from bs4 import BeautifulSoup
# 수푸 가져오기

html = """
    <html>
        <body>
            <ul>
                <li><a href='http://www.naver.com'>네이브</a></li>
                <li><a href='http://www.daum.net'>다아음</a></li>
            </ul>
        </body>
    </html>
"""

''' 리스트(li)목록의 내용과 해당 경로를 추출하기
    속성추출 : attrs['속성명']

    [출력결과]
    네이브 : http://www.naver.com
    다아음 : http://www.daum.net
'''
soup = BeautifulSoup(html,'html.parser')

a = soup.find_all('a')

for i in range(len(a)):
     href = i.attrs['href']
     print(f'{i+1}번 데이터 값 = {a[i].text} : {href}')

