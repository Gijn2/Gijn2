from bs4 import BeautifulSoup
import requests

url ='https://www.seoul.go.kr/seoul/autonomy.do'
site = requests.get(url)  # response 200 = 연결 성공 (content & string 의 차이)

bs = BeautifulSoup(site.content,'html.parser')

구청이름 = []
구청주소 = []
구청전화번호 = []
구청홈페이지 = []
# 1. 각 변수 리스트에 해당 하는 값을 저장 
for i in range(1,26): # 1 ~ 25
    name = bs.select('#district%d strong' % i)  # attrs 쓰기 구ㅣ 찮았음
    temp = bs.select('#district%d li' % i)
    #print(temp[0].text) # strong tags are printed
    #print(name[0].text,temp)
    #print(temp[0].text,temp[1].text,temp[2].text)

    구청이름.append(name[0].text)
    구청주소.append(temp[0].text)
    구청전화번호.append(temp[1].text)
    구청홈페이지.append(temp[2].text)

# 2. 출력
for i in range(25):
    print(f'구청이름  : {구청이름[i]}')
    print(f'구청 주소 : {구청주소[i]}')
    print(f'구청 전화번호 : {구청전화번호[i]}')
    print(f'구청 홈페이지 : {구청홈페이지[i]}')
    print('='*100)