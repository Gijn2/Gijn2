import requests,time,folium,pymysql,json

from selenium import webdriver
from selenium.webdriver.common.by import By # By만 쓸 수 있게끔 설정해주는 방법(간소화 해주는 작업)
from selenium.webdriver.chrome.options import  Options
from selenium.webdriver.chrome.service import  Service
from webdriver_manager.chrome import ChromeDriverManager

# Dbeaver에 PaulBassett table 생성 [데이터 받고 저장하는 동안 Dbeaver 켜서 테이블 확인 부탁.]
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

# selenium ==============================================================================================
options = Options()
options.add_experimental_option("detach",True)
serice = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options)

# 크롤링 변수 설정
url = 'https://www.baristapaulbassett.co.kr/store/Store.pb'
site = requests.get(url)

# 1-1. paul bassett 페이지 접근
driver.get(url)
time.sleep(3)  # 충돌 방지를 위한 딜레이

# data라는 리스트에 동적 리스트 값 담기
find_ul = driver.find_element(by=By.ID,value='shopList')
data_list = find_ul.find_elements(By.CSS_SELECTOR,'li')
data = []

for i in data_list:
    data.append(i.text)

# data에 저장된 값에 각 해당하는 값을 따로 저장
name = []       # 이름/매장명
tel = []        # 매장 번호
location = []   # 매장 주소
loc_lat = []    # 위도
loc_lon = []    # 경도

for j in range(len(data)):
    split_data = data[j].split('\n')
    name.append(split_data[0])
    tel.append(split_data[3])
    location.append(split_data[1])

# 1-2. 위도/경도 추출을 위한 화면 연결 및 진행
for k in range(len(data)):
    url2 = 'https://www.findlatlng.org/'
    driver.get(url2)
    driver.find_element(By.CLASS_NAME,'form-control').send_keys(location[k])
    driver.find_element(By.CLASS_NAME, 'btn').click()
    time.sleep(0.6)

    # 가져온 정보 잘라서 원하는 정보만 만드는 과정
    loc_info = driver.find_element(By.CLASS_NAME, 'container-fluid').text.split('\n')[1].split(' ')
    loc_lat.append(loc_info[2])
    loc_lon.append(loc_info[-1])
driver.quit()

# folium : 지도 생성 및 DB 저장 ==============================================================================================
map_osm = folium.Map(location=[loc_lat[0], loc_lon[0]]
                     , zoom_start=15
                     , zoom_control=True)
for l in range(len(data)):
    # print(f'이름 : {name[l]}, 번호: {tel[l]}, 주소 : {location[l]}, 위도 : {loc_lat[l]}, 경도 : {loc_lon[l]}')
    sql = """
       INSERT IGNORE INTO PaulBassett(shop_name,shop_tel,shop_addr,shop_lat,shop_long)
       VALUES (%s, %s, %s, %s, %s);
       """
    cursor.execute(sql, (name[l],tel[l],location[l],loc_lat[l],loc_lon[l]))

    conn.commit()

    folium.Marker(location=[loc_lat[l], loc_lon[l]]
                , popup=folium.Popup('''
                <dl>
                    <dd> 매장명 : {} </dd>
                    <dd> 연락처: {}  </dd>
                    <dd> 주소 : {}  </dd>
                </dl>'''.format(name[l],tel[l],location[l]),max_width=250,height=250)
                , icon= folium.Icon(color='blue',icon='info-sign')).add_to(map_osm)
map_osm.save('./cafe/PaulBassett_map.html')
conn.close()
print('지도 생성 / DB 종료')  # Dbeaver에서 테이블 생성되었는지 확인.=========