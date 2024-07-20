"""
 [ 제어문 ]
    - 파이썬은 들여쓰기를 하여 블록{}을 대신 표현한다
    - 들여쓰기는 탭과 공백을 섞어 쓰지 말자

    [JAVA]
    if (a>b) {
                                 명령어 a;
            명령어 b;
                    명령어 c;
    ** 관계없다. **
    }

    [ex]
    if a>b:
        print(a)
            print(b)  => 에러발생

    (1) if 문
        if 조건식A :
            문장들
        elif 조건식B :
            문장들
        else :
            문장들

        ` 조건식이나 else 뒤에는 콜론(:) 표시
        ` 조건식을 ( ) 괄호 필요없다
        ` 실행할 코드가 없으면 pass
        ` 파이썬은 switch 문 없음
"""

# 거짓(False)의 값
i = 0;
i2=0.0
i3=""
i4=str()
i5=list()
i6=tuple()
i7=set()
i8=dict()
i9={}
i10=None

if i:
    print('True')
else:
    print('False')

# 코딩 상에서 -1은 True
a = -1
if a:
    print('True2')
else:
    print('False2')

# if 문에서 not 사용가능
if not a:
    print('True3')
else:
    print('False3')

a = 10
b = 0

if a and b:
    print('True4') # 10은 True 지만 0은 False이므로 두 값 중 하나라도 False이므로 출력 X

if a or b :
    print('True5') # 10은 True 지만 0은 False이므로 두 값 중 하나라도 True이므로 출력

print( a and b ) => 0  # = 10 True, 0 False 이므로 하나라도 true 이므로 10출력
print( a or b )  => 10 # = 10 True, 이므로 하나라도 true 이므로 10출력

imsi = 0
if imsi:
    print('A')

    print('B')  # 들여쓰기가 안된 상황: if 문 안에 포함이 안됨.
print('C')      # 들여쓰기가 안된 상황: if 문 안에 포함이 안됨.

"""
[Error case 1]
if imsi:
    print('A')

print('B')  # 들여쓰기가 안된 상황: if 문 안에 포함이 안됨.
        print('C')      # 들여쓰기가 안된 상황: if 문 안에 포함이 안됨.


[Error case 2]
if imsi:
        print('A')

    print('B')  # 들여쓰기가 안된 상황: if 문 안에 포함이 안됨.
print('C')      # 들여쓰기가 안된 상황: if 문 안에 포함이 안됨.


[Error case 3]
if imsi:
    print('A')

print('B')  # 들여쓰기가 안된 상황: if 문 안에 포함이 안됨.
    print('C')      # 들여쓰기가 안된 상황: if 문 안에 포함이 안됨.
"""