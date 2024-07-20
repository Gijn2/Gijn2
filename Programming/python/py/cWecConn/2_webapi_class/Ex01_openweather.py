"""
    전세계날씨제공 API : http://openweathermap.org

    1. 회원가입 : 메뉴 > Sign Up > 사용용도 : Education > 대충가입 (무료는 1번에 60번 호출 가능 )
    2. 개발자모드 : Sign In > API Keys 에서 내가 발급받은 키 (추가 키 가능)
    3. 발급받고 바로 지정 안됨 (시간소요)
"""
import requests,json

# API 키를 지정합니다. 자신의 키로 변경해서 사용해주세요.
apikey = "1db47184ebbc18af53fd996be840d270"

# 날씨를 확인할 도시 지정하기
cities = ["Seoul,KR", "Tokyo,JP", "New York,US"]

# url 지정
api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

# 켈빈 온도를 섭씨 온도로 변환하는 함수
# k2c = lambda k: k - 273.15 , lambda를 비권장
def k2c(k):
    return round(k-273.15,3)

for cname in cities:
    url = api.format(city=cname, key=apikey)
    # print(url)

    res = requests.get(url)
    #print(res.text)     # 문자열로 받음.

    data = json.loads(res.text) # 받은 문자열을 json 구조로 올리기. -> dictionary

    print('도시 : {}, 날씨 상태 : {}, 최고 날씨 {}, 최저기온 : {} \n습도 : {}, 기압 : {}, 풍속 : {}'.format(data['name'],data['weather'][0]['description'],k2c(data['main']['temp_max']),k2c(data['main']['temp_min']),data['main']['humidity'],data['main']['pressure'],data['wind']['speed']))
    print('='*50)
