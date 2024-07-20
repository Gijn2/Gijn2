"""
csv : common string value
-> excel 에서 파일을 읽을 수 있기 때문에 (웹 크롤링, 빅데이터 -> 머신러닝, 알고리즘 등에 추후에 활용됨)

샘플을 추출해서 빅데이터 활용에 쓰기위해 excel활용을 해야만한다.

"""
import csv

# 1. list data 를 csv로 저장
"""
data = [[1,'강','연구원'],[2,'박','박주임'],[3,'김','김과장']]    

with open('./data/imsi.csv','at',encoding='utf-8') as f:   # wt의 경우 기존의 파일이 없으면 생성 xt는 기존의 파일이 있어서 error, at
    cout = csv.writer(f)    # csv 필터링을 씌운 f를 cout이라고 지칭
    cout.writerows(data)
"""

# 2. csv 파일을 읽어서 리스트에 저장

result = []

with open('./data/imsi.csv','rt',encoding='utf-8') as f:
    cin = csv.reader(f) #csv reader로 필터링
    result = [ row for row in cin if row] # 2-2. if row 를 추가해서 불필요한 빈 공간을 없애준다.(가비지 처리)


print(result)   # 2-1. 불필요한 빈공간이 생성되어 있음. -> 불필요한 요소(가비지) 처리: