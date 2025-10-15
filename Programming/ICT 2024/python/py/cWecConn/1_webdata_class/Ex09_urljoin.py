"""
 urllib.parse.urljoin() : 상대경로를 절대경로로 변화하는 함수
"""

baseUrl = 'http://www.example.com/html/a.html'

from urllib import parse as p
print(p.urljoin(baseUrl,'b.html'))      # baseUrl 에 b.html 더하려한다. -> a.html 이 b.html로 교체됨.
print(p.urljoin(baseUrl,'../b.html'))   # baseUrl 의 부모파일인 html에 b.html을 join

print(p.urljoin(baseUrl,'sub/c.html'))
print(p.urljoin(baseUrl,'/sub/c.html')) # 상대경로와 기본경로를 알자

# print(p.urljoin(baseUrl,'/temp/test.html')) # http://www.example.com/temp/test.html
# print(p.urljoin(baseUrl,'../temp/test.html')) # http://www.example.com/temp/test.html

print(p.urljoin(baseUrl,'https://www.other.com/mysite')) # 완전 다른 url을 가져오면 무시된다.
print(p.urljoin(baseUrl,'//www.other.com/mysite'))
print(p.urljoin(baseUrl,'www.other.com/mysite'))         # 앞에 아무것도 없으면 url을 자식으로 받는다.