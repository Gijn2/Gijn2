
# ------------------------------------------------------
"""
   (2) for문
        for <타켓변수> in 집합객체 :
            문장들
        else:
            문장들

        ` 반복문 뒤에 else는 반복하는 조건에 만족하지않으면 실행

   (3) while 문
        while 조건문 :
            문장들
        else :
            문장들

"""
a = 112                  # 숫자형
b = ['1','2','3']       # 리스트
c = '987'                # 문자열
d = tuple(b)             # 튜플
e = dict(k=5, j=6)       # 딕셔너리

for entry in e.items():
    # [범위]: a는 반복이 안되지만 b부터 e까지는 반복된다. : in 뒤에 나오는 건 집합이면 가능하다.
    # e - key value의 경우, 따로 값을 추출하고 싶을 경우 .items()를 사용

    print(entry)
    print('key : ',entry[0],', value : ',entry[1])
else:
    print('종료')

print('______________________________________________________')
# 처음부터 key value의 변수를 쪼개서 받아서 출력하기
for k,v in e.items():
    print(k,v)


# 1부터 10까지의 합
sum = 0
for i in range(1,11): # 숫자 범위를 잡아주는 range
    sum += i

    print('sum= ',sum)

# while
a = ['x','y','z']
while a:
    data = a.pop() # 스택구조로 뒤에서부터 하나씩 빼낼 예정
    print(data)

    if data == 'y':break
    # 도중에 반복문을 나갈 수 있게 break를 걸어줄 수 있다.

else:
    print('end')
    
"""
[과제] 2단부터 9단까지 이중 반복문으로 출력
"""
