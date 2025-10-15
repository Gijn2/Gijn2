msg = '행복해'            # 문자열
li = ['a','b','c']       # 리스트
tpl = ('ㄱ','ㄴ','ㄷ')    # 튜플
di = {'k': 5, 'j': 6, 'l':7 }    # 딕셔너리

# unpacking ( 요소분해 )
x,y,z = msg
print(x)
print(y)
print(x)

#
# alist = [[1,2],[3,4],[5,6]]
alist = [(1,2),(3,4),(5,6)]
for temp in alist:
    print(temp)

for first,second in alist:
    print('{} * {} = {}'.format(first,second,first*second))
    # python의 장점: 다른 코딩에 비해 수월하다.

"""
[과제] 2단부터 9단까지 이중 반복문으로 출력
"""

# enumerate 함수: 각 요소와 인덱스를 같이 추출
user_list = ['개발자','코더','전문가','분석가']
for value in user_list:
    print(value)

for value in enumerate(user_list):
    print(idx, value)


# zip 함수 :
days = ['월','화','수']
doit = ['잠자기','공부','놀기','밥먹기']
month = [5,6,7]

#print(zip(days,doit))
print(list(zip(days,doit,month)))
#print(dict(zip(days,doit)))