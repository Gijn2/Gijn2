# 파이썬 복습 - 기본규칙
"""
    - 들여쓰기는 4스페이스 (1 tab)
    - 한 줄은 최대 80자 이내로
    - 불필요한 공백은 피함
 """

# PEP8 규칙 (가능한 지켜야하는 코딩방식)
"""
    - 연산자는 1칸 이상 띄우지 않음
    - 변수명에 소문자 l(엘), 대문자 O(오), 대문자 I(아이) 는 금지
    lIOO = 100 (엘아이오오)

    - 주석은 항상 갱신하고 불필요한 주석은 삭제
    - 함수명은 소문자로 구성하고 필요하면 밑줄로 나눈다
"""

print("hello world") #실행방법 : ctrl + shift + f10

print("t"
      "e"
      "s"
      "t"
        )

print(""" 
        이게
      되네
      ㅋㅋ
""")

# python 기초지식
"""
    [datatype]
    1. 기본 자료형
        - 숫자형
        - 문자형
        - 논리형
        - 날짜형
    
    2. 집합 자료형
        - list
        - set
        - dictionary
        - ** tuple

    [variable / 변수] : 파이선의 모든 자료형은 객체로 취급

    ex. a = 7

    [숫자형]
    - 정수형 / 실수형

    정수형(int) : 소수점이 없는 정수 (파이썬은 매우 큰 정수도 정확하게 처리할 수 있음)
    
    <연산기호> : + - * / % // **

    실수형(float) : 소수, 유한한 자릿수로 표현되기 때문에 정밀도에 한계가 있을 수 있습니다.

    ex. pi = 3.14159
        radius = 5
        area = pi * radius * radius

        print(area)

    
    **기타 숫자형 - 복소수(허수) : 실수 부분과 허수 부분으로 구성된 수
                 - bool (논리) : true or false를 나타내는 값(숫자 연산 시, 0 or 1로 취급될 수 있음.)
    
                 

    [키워드] : 파이썬에도 키워드는 존재한다.
    import keyword

    print(keyword.kwlist) # 키워드 호출방법
    print("키워드의 개수는 ", len(keyword.kwlist))

    print(id(a))    # 주소값을 불러오는 함수 : id()

    a,b = 5,10 # 다중 변수선언

    print("a,b =", a, b) # 정상 출력
    del b
    # print(b) --> 에러 발생

"""