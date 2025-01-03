"""
# Path는 파일 시스템에 접근하기 때문에, 기본적으로 운영체제 상에 조작 대상 파일 경로가 존재해야 합니다.
# PurePath는 순수 경로의 기반 클래스입니다.
# 파일 시스템에 접근하지 않기 때문에, 운영체제 상에 존재하지 않는 파일 경로를 다룰 수도 있습니다.
"""

#-------------------------------------------------------------------
# 1 - 존재하지 않는 경로

from pathlib import PurePath

j = PurePath('babo/myclass/myjob') # 거짓경로를 임의로 지정
print(j)
print(j.parts) # 경로 쪼개기


j = PurePath('e:/babo/myclass/myjob')
print(j)
print(j.parts)
#-------------------------------------------------------------------
# 2. 실제 경로로 아닌 가짜 경로를 관리하는 PurePath를 어디에 사용할까?
# 아마도 경로나 파일명만 조작할 때 사용하지 않을까?
# 해당 경로나 파일명이 현재 컴퓨터가 아니기에 이름만 관리하는 작업이 필요할 듯 싶다
# ex.

j=PurePath('\\192.168.0.22\Share\itc')
print(j)
print(j.parts)

print('='*100)

j1 = PurePath('C:\Windows\System32\drivers\etc\hosts')
print(j1.parts)
print(j1.parts[0])
print(j1.parts[3])

print(j1.parents[0])
print(j1.parents[1])
print(j1.parents[2])