import requests,time,folium,pymysql,json

from selenium import webdriver
from selenium.webdriver.common.by import By # By만 쓸 수 있게끔 설정해주는 방법(간소화 해주는 작업)
from selenium.webdriver.chrome.options import  Options
from selenium.webdriver.chrome.service import  Service
from webdriver_manager.chrome import ChromeDriverManager
# from geopy.geocoders import Nominatim -> 사라짐.

# 크롤링 변수 설정
url = 'https://www.baristapaulbassett.co.kr/store/Store.pb'
site = requests.get(url)

# 셀레니움 설정
options = Options()
options.add_experimental_option("detach",True)

serice = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options)

# 페이지 접근
driver.get(url)
time.sleep(2)               # 홈페이지를 불러오면서 충돌 방지를 위해 딜레이 걸어주기

find_ul = driver.find_element(by=By.ID,value='shopList')
data_list = find_ul.find_elements(By.CSS_SELECTOR,'li')

# data라는 리스트에 동적 리스트 값 담기 및 확인
data = []
for i in data_list:
    data.append(i.text)

# data에 저장된 값에 각 해당하는 값을 따로 저장
name = []       # 이름/매장명
tel = []        # 번호
location = []   # 주소
loc_lat = []    # 위도
loc_lon = []    # 경도
"""
def get_location(loc_info):
    try:
       geolocoder = Nominatim(user_agent='South Korea', timeout=None)
       geo = geolocoder.geocode(loc_info)
       crd = {"lat":str(geo.latitude), "lng":str(geo.longitude)}

       loc_lat.append(crd["lat"])
       loc_lon.append(crd["lng"])
    except Exception as e:
        print('get_location 오류 : ',e)
"""
for j in range(len(data)):
    split_data = data[j].split('\n')
    name.append(split_data[0])
    tel.append(split_data[3])
    loc_info = split_data[1]
    location.append(loc_info)
    # get_location(loc_info)

    # print(split_data) # 데이터 확인
    print(f'이름 : {name[l]}, 번호: {tel[l]}, 주소 : {location[l]}, 위도 : {loc_lat[l]}, 경도 : {loc_lon[l]}')
driver.quit()


# 지도 저장 ==============================================================================================
# 데이터 확인 및 지도에 위치 저장 (cafe 라는 디렉토리 생성해야함.)
print('1.',loc_lat,len(loc_lat),len(name))
print('2',loc_lon,len(loc_lon))
map_osm = folium.Map(location=[loc_lat[0], loc_lon[0]]
                     , zoom_start=15
                     , zoom_control=True)
for l in range(len(data)):
    try:
        folium.Marker(location=[loc_lat[l], loc_lon[l]]
                    , popup=folium.Popup('''
                    <dl>
                        <dd> 매장명 : {} </dd>
                        <dd> 연락처: {}  </dd>
                        <dd> 주소 : {}  </dd>
                    </dl>'''.format(name[l],tel[l],location[l]),max_width=250,height=250)
                    , icon= folium.Icon(color='blue',icon='info-sign')).add_to(map_osm)
    except Exception as e:
        print(e)
map_osm.save('./cafe/PaulBassett_map_test.html')
print('지도 생성 완료')

'''
# DB 저장 ==============================================================================================
# Dbeaver에 PaulBassett 이라는 table 생성
conn = pymysql.connect(host='localhost',
                       user='scott',
                       password='tiger',
                       db='basic',
                       charset='utf8')
cursor = conn.cursor()
sql = sql = """
CREATE TABLE IF NOT EXISTS PaulBassett(
    shop_name VARCHAR(100) NOT NULL PRIMARY KEY,
    shop_tel VARCHAR(100) NOT NULL,
    shop_addr VARCHAR(100) NOT NULL,
    shop_lat DOUBLE NOT NULL,
    shop_long DOUBLE NOT NULL
);
"""
cursor.execute(sql)

# Dbeaver에서 테이블 생성되었는지 확인.===========================================
# 데이터 확인 및 데이터 table에 주입
for l in range(len(data)):
    # print(f'이름 : {name[l]}, 번호: {tel[l]}, 주소 : {location[l]}, 위도 : {loc_lat[l]}, 경도 : {loc_lon[l]}')
    sql = """
       INSERT IGNORE INTO PaulBassett(shop_name,shop_tel,shop_addr,shop_lat,shop_long)
       VALUES (%s, %s, %s, %s, %s);
       """
    cursor.execute(sql, (name[l],tel[l],location[l],loc_lat[l],loc_lon[l]))

    conn.commit()
'''
print('DB 종료')
