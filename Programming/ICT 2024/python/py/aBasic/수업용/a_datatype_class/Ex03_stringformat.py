a = '홍길동'
print(a+"hi") # 문자열 연결
print(a,"hi") # 문자열 과 문자열 사이에 띄어쓰기가 존재 [비추]

# -----------------------------------------
#  문자열 포맷
#       0- 문자열 포맷팅
#               print('내가 좋아하는 숫자는 ', 100 )
#       1- format() 이용
#               print('내가 좋아하는 숫자는 {0:d} 이다'.format(100) )
#       2- % 사용
#               print('내가 좋아하는 숫자는 %d 이다' % 100 )
#       성능(속도)는 %이 더 빠르다고는 하지만 코드가 깔끔하게 하는 것이 더 중요하다고 하고는
#       어느 것으로 선택하라고는 안 나옴

# format()이용
msg = '{}님 오늘도 행복하세요.'
print(msg.format('홍길자'))
print(msg.format('홍길동동'))

msg = '{}님 오늘도 행복하세요. - {}가'
#print(msg.format(*args:'홍길동','ict'))

msg = '{0}님 오늘도 행복하세요. - {1}가'
#print(msg.format(*args:'홍길동','ict'))

msg = '{1}님 오늘도 행복하세요. - {0}가'
#print(msg.format(*args:'홍길동','ict'))

msg = '{name}님 오늘도 행복하세요. - {group}가'
print(msg.format(name='홍길동', group='ICT'))
print(msg.format(name='ICT', group='홍길동'))

# [참고] http://pyformat.info
# % 이용 - printf() 역할
name = '홍길동'
age = 22
height = 170.456
print('%s 님은 %d 살이고 신장은 %f cm 입니다.' % (name, age, height))

# --------------------------------------------------------------------------
# 실수인 경우

su = 99.99
print('내가 좋아하는 수는 {:.1f}입니다'.format(su))  # 소수점 하나로 만들면 강제로 반올림 처리 (0 생략 가능)
print('내가 좋아하는 수는 %.2f입니다' % su)          # %의 경우 소수점 이하 6자리까지 무조건 출력 -> 다음과 같이 0.2를 넣어주어 소수점 위치 처리

fact = "Python is funny"
print(str(fact.count('n') + fact.find('n') + fact.rfind('n')))

text = 'Gachon CS50 - programming with python'
print(text[-1])