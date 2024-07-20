'''
[ 1단계 수집시스템 ] 조별로 통닭 & 커피 프랜차이즈 중 하나를 선택
웹페이지에서 매장명,전화번호,주소를 크롤링하여
DB에도 저장하기
( 오라클 or mariadb or mysql )
-----------------------------------
매장명 | 전화번호 | 주소 | 위도 | 경도
name  | tel    | addr | latitude | longitude
가산 | 02-2222 | 신촌동 |    |
'''
'''
[ 2단계 저장시스템 ] DB에 위도,경도 컬럼을 추가
주소를 입력하면 위도,경도를 알수 있는 웹API를 연결하여
해당 주소의 경도, 위도를 DB에 입력
ex) https://www.findlatlng.org/
ex) https://www.vworld.kr/dev/v4api.do
-----------------------------------
매장명 | 전화번호 | 주소 | 위도 | 경도
name  | tel    | addr | latitude | longitude
가산 | 02-2222 | 신촌동 | 11111.11 | 222222.22

* 해당 주소에 위도, 경도가 안 나올 수도 있음
'''

import pymysql, requests, folium, time
import csv, re, os
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# =====================================================================
# Kakao Map API 키
KAKAO_API_KEY = '1fd3c408a829ebf6635e1f44016cfdb6'


def get_lat_lng(address):
    # Kakao Map API 호출을 위한 URL
    url = f'https://dapi.kakao.com/v2/local/search/address.json?query={address}'

    # API 호출
    headers = {'Authorization': f'KakaoAK {KAKAO_API_KEY}'}
    response = requests.get(url, headers=headers)
    data = response.json()

    # 결과 확인
    if data['documents']:
        latitude = data['documents'][0]['y']
        longitude = data['documents'][0]['x']
        return latitude, longitude
    else:
        return None, None


# ===========================================================

# 2. 데이터베이스에 연결
connection = pymysql.connect(
    host='192.168.0.210',
    user='seoulinfo',
    password='seoul',
    db='seoulinfo',
    charset='utf8'
)

print('Database connection successful')

try:
    cursor = connection.cursor()

    # 지도에 Marker 설정
    sql = "SELECT evc_name, evc_lat, evc_long FROM evc"
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)

    # 지도 객체 생성
    map_osm = folium.Map(location=[37.572807, 126.975918], zoom_start=12)

    for name, latitude, longitude in rows:
        if latitude is not None and longitude is not None:
            folium.Marker(location=[latitude, longitude]
                          , popup=name
                          , icon=folium.Icon(color='blue', icon='info-sign')).add_to(map_osm)

    map_osm.save('./map/ev2.html')

    print('Data successfully written to MySQL table')


finally:
    # 데이터베이스 연결 닫기
    connection.close()
    print('Database connection closed')

# 드라이버 종료
# driver.quit()
