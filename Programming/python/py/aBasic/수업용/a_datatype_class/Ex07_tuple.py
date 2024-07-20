"""
#----------------------------------------------------------
[튜플 자료형]
    1- 리스트와 유사하지만 튜플은 값을 변경 못한다.
    2- 각 값에 대해 인덱스가 부여
    3- [아주 중요함.]변경 불가능 (*****)
    4- 소괄호 () 사용

    JAVA 에서 불가능했던걸 가능하게 해준다
"""

# (1) 튜플 생성
print('------------------- 1. 튜플 생성-----------------')
t = [1,2,3] # list
t = {1,2,3} # set
t = (1,2,3) # tuple

print(t)
print(type(t))
print(t[0])     # list와 동일한 취급
print(t[1:])    # list와 부분적인 호출 및 사용법 모두 적용가능 // 차이점: tuple은 값이 변경 불가능, list는 값 변경 가능

t2 = 8,9,0 # 권장하지않음 절대 소괄호 써줘
print( t2 )

# (2) 튜플은 요소를 변경하거나 삭제 안됨
# t[1] = 0 -> IndentationError: unexpected indent 발생
# del t[1] -> IndentationError: unexpected indent

del t
print('확인') # 가능.튜플-자체 삭제(<-)와 안의 요소 삭제 및 변경(위)은 다른 것

print('------------------- 2 -----------------')


# (3) 하나의 요소를 가진 튜플
print('------------------- 3 -----------------')
t3 = (1)
print(t3)
print(type(t3))    # 왜 ( )는 tuple일텐데 int형인가? -> 여기서 ( ) 는 우선순위로 취급

# *****************************************************************
t4 = (1, )         # 요소를 하나만 가진 tuple을 만들고싶을때 작성 방법
print(t4[0])
print(type(t4))     # type = tuple

# (4) 인덱싱과 연산자 : list와 동일
print('------------------- 4 -----------------')
t = (1,2,3,4,3,5,6,1)
print(t)
print(t[2]) # 2번 추출
print(t[3:])
print(t[:-3])
print(t[:4])

t2 = (1,2,3)
print(t+t2)
print(t2*3)

