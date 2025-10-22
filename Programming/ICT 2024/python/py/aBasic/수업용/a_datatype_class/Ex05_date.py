"""
import datetime
today = datetime.date.today();
print('today is ', today)
"""

# 날짜를 가져오는 datetime으로부터 설정해버리기
from datetime import date, timedelta
today = date.today()
print('today is ',today)

# 년도 구하기
print('년 :',today.year)

print("월 : ",today.month)

print("일 : ",today.day)

print("요일 : ",today.weekday())    # Monday = 0
print("요일 : ",today.isoweekday()) # Monday = 1

# 날짜 계산
#from  datetime import  timedelta

print('어제 : ',today+timedelta(days=-1))
print('3주 전 : ',today+timedelta(weeks=-3)) #weeks
print('10일 후 : ',today+timedelta(days=+10))

"""
한 달 후 or 1년 이후: dateu%til 패키지 이용( 따로 설치 필요 )
"""
# 날짜형과 문자열 형식 변환하기
from datetime import datetime
today = datetime.today()
print(today)

# 날짜형 -> 문자형 변환 : strftime() 이용
print(today.strftime('%m, %d, %y'))

# ----년 -월 -일 --시 --분
print(today.strftime('%y년%m월(%h)%d일%H시%M분'))

# 문자열 -> 날짜형 : strptime() 이용
naljja = '2024-05-24 12:04:49'
print(type(naljja))

mydate = datetime.strptime(naljja,'%Y-%m-%d %H:%M:%S')
print(mydate)
print(type(mydate))