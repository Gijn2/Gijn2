
# urlretrieve(): 파일로 바로 저장
# urlopen(): 파일로 바로 저장하기 않고 메모리에 로딩을 한다.

""" [참고] 파일저장 기본방식
    f = open('a.txt','w')
    f.write("테스트 내용")
    f.close()

    위의 과정을 with 문으로 간략하게 close 필요없음
    with open("a.txt","w") as f:
        f.write("테스트 내용")
"""

from urllib import request

url = 'https://www.google.co.kr/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'
imgName = 'data/daum.png'

site = request.urlopen(url)
page = site.read()

with open(imgName,'wb') as f:   # wb: write binary, 이미지 경로를 읽어서 그 파일을 내 파이썬 파일에 저장
    f.write(page)