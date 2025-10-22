# 내장 모듈 - request(주의, requests - request 혼동하지않기)

from urllib import request

url = 'https://www.google.com'

site = request.urlopen(url) # Stream open
page = site.read()
print(page)                 # content와 동일
print('='*100)

print(site.status)          # 주고받은 신호값 출력
print('='*100)

for h in site.getheaders():
    print(h)                # tuple 형태로 key,value 출력

