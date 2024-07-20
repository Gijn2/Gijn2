from bs4 import BeautifulSoup
from urllib import  request

url = 'https://www.yes24.com/Product/Search?domain=ALL&query=python'
html = request.urlopen(url)

soup = BeautifulSoup(html,'html.parser')

# 책 제목 추출
titles = soup.select('ul#yesSchList .info_name > a.gd_name')
for i in titles:
    print("{}".format(i.text))

print('='*100)
# 책 이미지  경로 추출
img = soup.select('img.lazy')

# 책 제목으로 해당 경로의 이미지 저장
for i in img:
    print(i.attrs['data-original']) # src가 아닌 data-original 태그 안에 진짜 경로가 저장되어 있따.
    print(i.attrs['alt'])           # 저장할 이미지 이름

    #request.urlretrieve(i.attrs['data-original'],imgName)

    # 책제목으로 해당 이미지를 파일로 저장하기
    request.urlretrieve(i.attrs['data-original'],'img/'+i.attrs['alt'].replace('/','_')+'.jpg')