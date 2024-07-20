"""
    @ 컴프리핸션 (comprehension)
    ` 하나 이상의 이터레이터로부터 파이썬 자료구조를 만드는 컴팩트한 방법
    ` 비교적 간단한 구문으로 반복문과 조건 테스트를 결합

    * 리스트 컨프리핸션
        [ 표현식 for 항목 in 순회가능객체 ]
        [ 표현식 for 항목 in 순회가능객체 if 조건 ]

    * 딕셔러리 컨프리핸션
        { 키_표현식: 값_표현식 for 표현식 in 순회가능객체 }

    * 셋 컨프리핸션
        { 표현식 for 표현식 in 순회가능객체 }

"""

"""
# 컨프리핸션 사용하지 않은 리스트 생성
alist = []
alist.append(1)
alist.append(2)
alist.append(3)
alist.append(4)
alist.append(5)
alist.append(6)
print(alist)

alist = []
for n in range(1,7):
    alist.append(n)
print(alist)

alist = list(range(1,7))
print(alist)
"""
#------------------------------------------------
# 리스트 컨프리핸션

# n ~ n 의 범위가 1 부터 7이전 까지
blist = [ n for n in range(1,7) ]
print(blist)

# n-1 ~ n 의 범위가 1 부터 차례 대로 7번 전까지
blist = [ n-1 for n in range(1,7) ]
print(blist)

blist = [ n*2 for n in range(1,7) ]
print(blist)

blist = [ n for n in range(1,7) if n%2 == 0]
print(blist)

#------------------------------------------------
# 셋 컨프리핸션
data = (1,2,3,3,2,4,5)

alist = [n for n in data]
print(alist)

aset = {n for n in data}
print(aset)

#-------------------------------------------
# 딕셔러니 컨프리핸션

datas = (2,3,4)
adic = {x:x**2 for x in datas}
print(adic)

word = 'LOVE LOL'

# wcnt = { letter for letter in word } 까지는 set
wcnt = { letter:word.count(letter) for letter in word } # 이렇게는 key value/ key value 로 처리
# word의 letter의 수를 세서
print(wcnt)

# -----------------------------------------------

print('-'*50)
clist = []
for r in range(1,4):
    for c in range(1,3):
        clist.append((r,c))
print(clist)

dlist = [(r,c)for r in range(1,4) for c in range(1,3)]
print(dlist)

print('-'*50)









# -------------------------------------------------
# [참고] 제너레이터 컨프리핸션
# ( ) 를 사용하면 튜플이라 생각하지만 튜플은 컨프리핸션이 없다.
















# -------------------------------------------------
# 프로젝트할 때 팀구호
#우리의결의= """취하고싶으면달려라
#맡은업무는반드시마치자
#노력없는성과는없다
#구글신과함께공부하자
#"""
#result = [ j[i*2] for i, j in enumerate(우리의결의.split('\n')]
#print(result)

num = ""

for i in range(10):
    if i <= 5 and (i % 2)==0:

        continue
    elif i is 7 or i is 10:

        continue
    else:

        num = str(i) + num
print(num)
# -4 가 아닌 이유 : -5이면 for문을 탈출하네(5 ~ -5이전까지) 고로 -5 +1을 안함
135689


3.
list = []
p = 0                       # 표준편차를 담을거에요
avg = 0                     # 평균을 담을거에요
for i in range(5):
    a = int(input('정수를 입력하세요 : '))
    list.append(a)
    avg += a       # 평균
print('입력하신 리스트 내역 : {}, 평균 : {}'.format(list ,avg/len(list)))
for list in len(list):
    p += (a - avg/len(list))**2     # 표-편

print('표-편{}'.format(p**0.5))

