"""
    [ dictionary 형 ]

    1- 키와 값으로 구성 ( 자바의 map 와 유사 )
    2- 저장된 자료의 순서는 의미 없음
    3- 중괄호 {} 사용
    4- 변경가능

    ` 사전.keys() : key만 추출 (임의의 순서)
    ` 사전.values() : value만 추출 (임의의 순서)
    ` 사전.items() : key와 value를 튜플로 추출 (임의의 순서)
"""

print('--------- 1. 딕셔너리 요소 --------------- ')
dt = {1:'one', 2:'two', '3':'three', 1:'하나',3:'셋'}
# 각 key에 값을 지정해준다., -> 한번 더 지정 시, key값을 덮어쓰기(java 와의 공통점)

print(dt) # key값 확인
print(dt[1]) #key값 중 1번 요소를 확인
print(dt[2]) #key값 중 2번 요소를 확인
print(dt['3'])
# print(dt[3]) key값 중 3번 요소를 확인 -> error: '3' 의 값으로 요청해야함 : key의 자료형도 따진다.
print(dt[3])


# 키는 숫자와 문자 그리고 튜플이여야 한다. 즉 리스트는 안된다.
# 리스트의  값이 변경 가능하다. 그러나 키값을 변경하면 안되므로 리스트는 안된다
dt2 = {1:'one', 2:'two', (3,4):'turple'}

# (3,4) 를 하나의 덩어리로 봐야한다.
print(dt2[(3,4)])

print('--------- 2. 딕셔너리 추가 및 수정  --------------- ')
# 딕셔너리에 값 추가 및 수정
dt2['korea'] = 'seoul'
print(dt2)
# 존재하는 값에 key를 주면 수정이 되고 존재하지않는 값에 key를 주면 추가가 된다.

# 여러개 추가할 때
dt2.update({5:'five',6:'six',7:'seven'})
print(dt2)

print('--------- 3. Key로 Value값 찾기  --------------- ')
# print(dt2[3]) : 에러발생 시, 더이상 실행하지 않음 -> 인터프리티 언어: 위에서 쭉 읽어 내려가는 프로그램 이기때문!
print(dt2.get(3)) # 위와같은 표시대신 다음과 같이 표시해주자. : none 이라고 표시
print(dt2.get(3,"키값 없음"))
print(dt2.get(6)) # 6이 기존에 존재하므로 six 라는 값을 호출
print(dt2.get(6,"키값 없음"))

print(dt2.keys())
print(dt2.values())
print(dt2.items())

# Key와 Value만 따로 검색
