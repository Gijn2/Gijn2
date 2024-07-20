"""
    파이썬에서 웹을 요청할 수 있는 라이브러리
        1- requests 라이브러리 (s붙음 주의) - 추가
            1-1. requests: 외부 모듈 = 추가를 해줘야 사용가능
            1-1. request : 기존의 내장 모듈
        2- urllib 라이브러리 - 내장모듈

    차이점
        1- requests는 요청 메소드(get/post)를 구분하지만 urllib는 보내는 데이타 여부에 따라 구분됨
        2- 데이타 보낼 때 requests는 딕셔러니 형태로 urllib는 인코딩한 바이너리 형태로 보낸다.
            2-1.
        
    requests 라이브러리 추가
    메뉴 > File > Settings > Project Interpreter > + 버튼 > 'requests' 검색 후 인스톨

[ requests 모듈 ]
(1) Rest API 지원
    import requests
    resp = requests.get('http://www.mywebsite.com/user')
    resp = requests.post('http://www.mywebsite.com/user')
    resp = requests.put('http://www.mywebsite.com/user/put')
    resp = requests.delete('http://www.mywebsite.com/user/delete')

(2) 파라미터가 딕셔너리 인수로 가능
    data = {'firstname':'John', 'lastname':'Kim', 'job':'baksu'}
    resp = requests.post('http://www.mywebsite.com/user', data=userdata)

(3) json 디코더 내장 (따로 json 모듈 사용 안해도 됨)
    resp.json()
"""

import requests
url = 'https://www.google.com'
res = requests.get(url) # get 방식, post는 무조건 form 태그가 필요함
print(res)               # 요청이 잘 받아지면 <response [200]>, get/post form 방식이 맞지 아니하면 <response [405]>, 아예 잘못 되었을 경우, error
print('-'*100)
print(res.text)          # JAVA라면 문자열로 받음 : UTF 파일
print('-'*100)
print(res.content)       # byte 객체로 받음 : 아스키 코드

print('-'*100)
print(res.headers)       # 구분자 : pyhton에서 dictionary -> JAVA 식: .json 형태로 나옴.

# key >> value
# Date >> Mon, 03 Jun 2024 00:53:35 GMT
print('-'*100)
for key,value in res.headers.items():
    print(f'{key}, {value}')
