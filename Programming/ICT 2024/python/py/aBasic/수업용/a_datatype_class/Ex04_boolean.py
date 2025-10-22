# 부울형 - 첫글자는 반드시 대문자 True, False, None 여야 한다
t = True
f = False
n = None    # 다른 언어의  null 값과 유사

hungry = True
sleepy = False
print(not sleepy)
print(type(hungry))

print(hungry & sleepy) # and = 하나라도 false면 false
print(hungry | sleepy) # or = 하나라도 true면 true
print(hungry and sleepy)
print(hungry or sleepy)



"""
        자료형         값           부울형
    -----------------------------------------------------
        문자형       "문자"          True
                    ""                     False
        리스트       [1,2,3]         True       
                    []                     False
        튜플         ()                     False
        딕셔너리     {}                     False
        숫자형       0이아닌 숫자     True
                    0                      False
                    None                   False

"""

""" 
#######################################
파이썬은 block 표시를 위한 { } 중괄호가 없음
    -> 줄 맞춤이 곧 괄호(block 처리): 줄 맞춤이 매우 중요
    ==> python은 들여쓰기로 block 표현
#######################################
"""
if('아'):
    print('True')
else:
    print('False')

if([]):
    print('True2')
else:
    print('False2')

if 0:
    print('True3')
else:
    print('False3')

if -1:
    print('True4')
else:
    print('False4')

# ===========================================
msg='행복합시다'

if msg.find('행'):  # 문자열에 존재하면 True / 없으면 False를 반환해줄 줄알았지
    print('True5')
else:
    print('False5') # 있는 값이라서 실수 값 반환 { n > 0 => False }
    
if msg.find('가'):
    print('True6')
else:
    print('False6') # 없는 값이라서 -1 반환     { n < 0 => True }

# =============================================

