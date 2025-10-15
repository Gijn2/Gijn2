from bs4 import BeautifulSoup
from urllib import request
from urllib.parse import quote
import re

url = 'http://www.pythonscraping.com/pages/warandpeace.html'
html = request.urlopen(url)

bs = BeautifulSoup(html,'html.parser')
green = bs.select('span.green')

# 중복을 제거하지 않은 경우
"""
for i in range (len(green)):
    print(f'녹색 문장 {i+1} 번 : {green[i].text} ')

print('-'*100)
"""
# 중복을 제거한 경우
for i in set(green):
    print(i.text)

# =========================================================
print('-'*100)

url2 = 'https://www.pythonscraping.com/pages/page3.html'
html2 = request.urlopen(url2)

bs2 = BeautifulSoup(html2,'html.parser')
cost = bs2.select('tr.gift td')

for i in range(len(cost[2::4])):
    print("이름은 : {}가격은 : {}".format(cost[0::4][i].text,cost[2::4][i].text))

# ========================================================
# 연습문제 3번
print('-'*100)

url3 = 'https://wikidocs.net/'
html3 = request.urlopen(url3)

bs3 = BeautifulSoup(html3,'html.parser')
title = bs3.select('h4.media-heading a')
writer = bs3.select('div.book-detail a.menu_link')
imglink = bs3.select('div.book-image-box img.book-image')

for i in range(len(title)):
    print(f' {i+1}번 책이름: {title[i].text}, 저자: {writer[i].text}')
    request.urlretrieve(url3+quote(imglink[i].attrs['src']),'./testimg/'+re.sub(r'[<>:"/\\|?*]', '',title[i].text)+'.png')
    print(imglink[i].attrs['src'],'저장 성공')

