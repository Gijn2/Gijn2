"""
    [ 콘솔 입력 처리 함수 ]
    - input() : 기본적으로 문자열로 입력받음
    - eval() : 함수로 감싸면 숫자 처리됨
    - int() / float() / str() 자료형변환  ( eval() 사용보다는 형변환을 권장 )

    eval() 함수는 남용하면 절대 안된다. 형변환을 가급적 사용하지 마라.
"""
# 나이 입력 후 출력하는 법
"""
name = input('이름을 입력하세요 : ')
print('1. 너의 이름은 ',name)
print('2. 너의 이름은 {} '.format(name))
print('3. 당신은 %s 입니다.' %name)
"""
#-------------------------------------------
#나이를 입력받아 +1을 하여 출력하고 키를 실수형으로 입력받아 출력
"""
age = int(input('나이를 입력하세요 : '))
print('당신의 나이는 {}'.format(age+1))
"""
#----------------------------------
# 단을 입력받아 구구단을 구하기
"""
num = int(input('단을 입력하세요 : '))
for i in range (1,10):
    result = num*i
    #print(i,'*',num,'=',result)
    print('{0} * {1} = {2} '.format(i,num,result) )
"""
#-----------------------------------------
# print() 함수
print('안녕'+'친구')
print('안녕','친구')
print('안녕' '친구') # 모두 가능한 표현

print('1')
for i in range(5):
    print(i) # 자동으로 개행이 일어남.

print('2')
for i in range(5):
    print(i,end='/') # 개행을 하고싶지 않을 경우 추가 작성

print('3')
for i in range(5):
    print(i,end=',' if i<4 else "") # if문: 마지막 행 뒤에는 비우겠다.

# -------------------------------------------------------
# 명령행 매개변수 받기 - java의 main() 함수의 인자
# [ 콘솔에서 실행 ] python Ex10_stdio.py ourserver scott tiger
#                                   0      1      2      3

