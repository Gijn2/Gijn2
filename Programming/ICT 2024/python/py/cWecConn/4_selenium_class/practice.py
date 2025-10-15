import requests,time,folium,pymysql,json

from selenium import webdriver
from selenium.webdriver.common.by import By  # By만 쓸 수 있게끔 설정해주는 방법(간소화 해주는 작업)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



# 크롤링 변수 설정

url = 'https://korean.visitkorea.or.kr/kfes/list/wntyFstvlList.do'
site = requests.get(url)

# 셀레니움 설정
options = Options()
options.add_experimental_option("detach",True)

serice = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options)

def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page
        time.sleep(3)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 페이지 접근
driver.get(url)
time.sleep(1)               # 홈페이지를 불러오면서 충돌 방지를 위해 딜레이 걸어주기
scroll_down(driver)

find_ul = driver.find_element(by=By.CLASS_NAME, value='other_festival_ul')
data_list = find_ul.find_elements(By.CLASS_NAME,'other_festival_content')

# data라는 리스트에 동적 리스트 값 담기 및 확인
data = []
for i in data_list:
    data.append(i.text)
print(data)

# data에 저장된 값에 각 해당하는 값을 따로 저장
name = []           # 축제 이름
location = []       # 축제 위치
period = []         # 축제 기간
start_date = []     # 축제 시작
end_date = []       # 축제 끝

for j in range(len(data)):
    try:
        split_data = data[j].split('\n')
        name.append(split_data[0])
        location.append(split_data[2])

        date = split_data[1]            # 날짜 추출
        period.append(date)
        split_date = date.split('~')    # 날짜 분리
        start_date.append(split_date[0])
        end_date.append(split_date[1])

        print(split_data)  # 데이터 확인
    except Exception as e:
        print('오류',e)

print(name)
print(len(name))
print(period)
print(len(period))
print(location)
print(len(location))
print(start_date)
print(len(start_date))
print(end_date)
print(len(end_date))

driver.quit()

"""
# 지도 저장 ==============================================================================================
# 데이터 확인 및 지도에 위치 저장 (cafe 라는 디렉토리 생성해야함.)
print('1.',loc_lat,len(loc_lat),len(name))
print('2',loc_lon,len(loc_lon))
map_osm = folium.Map(location=[loc_lat[0], loc_lon[0]]
                     , zoom_start=15
                     , zoom_control=True)
for l in range(len(data)):
    try:
        print(f'이름 : {name[l]}, 번호: {tel[l]}, 주소 : {location[l]}, 위도 : {loc_lat[l]}, 경도 : {loc_lon[l]}')
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
"""


# DB 저장 ==============================================================================================
# Dbeaver에 PaulBassett 이라는 table 생성
conn = pymysql.connect(host='localhost',
                       user='scott',
                       password='tiger',
                       db='basic',
                       charset='utf8')
cursor = conn.cursor()
sql = sql = """
CREATE TABLE IF NOT EXISTS FestivalBoard(
   festnum 	INT	AUTO_INCREMENT PRIMARY KEY
	,name		varchar(100)
	,period 	varchar(100)
	,location	varchar(100)
	,startDate  varchar(100)
	,endDate    varchar(100)
);
"""
cursor.execute(sql)

# Dbeaver에서 테이블 생성되었는지 확인.===========================================
# 데이터 확인 및 데이터 table에 주입
for l in range(len(name)):
    sql = """
       INSERT IGNORE INTO FestivalBoard(name,period,location,startDate,endDate)
       VALUES (%s, %s, %s, %s, %s);
       """
    cursor.execute(sql,(name[l],period[l],location[l],start_date[l],end_date[l]))

    conn.commit()

print('DB 종료')
