from pathlib import Path

# ------------------------------------------------
# 1. 경로의 상태보기
print(Path.cwd())  # C드라이브?
print(Path.home()) # home 디렉토리?
"""
    리눅스인 경우,
         root 로그인 한 경우, - /root
         centos 로그인의 경우, - /home/centos
         abc 로그인 한 경우 - /home/abc
"""

# ----------------------------------------------------
# 2. 경로(파일) 생성시간 알아보기
p1 = Path('Ex03_createPath.py')
p1.stat()                           # 경로의 상태값들이 나온다. 이 중 st_ctime이 생성시간을 알 수 있는 상태값
ctime = p1.stat().st_ctime
print(ctime)                        # 알 수 없는 정보가 나와버렸다.
print('='*100)

from datetime import datetime       # 이 정보를 우리가 알 수 있는 시간으로 가공해주기 위해 불러오는 시간
ctimeResult = datetime.fromtimestamp(ctime)
print(ctimeResult)

# ------------------------------------------------
# 3. 디렉토리 생성
p1 = Path('imsi')
p1.mkdir(exist_ok=True)              # exist_ok = True : 존재하지 않을 경우, 생성/ 존재할 경우, 생성 X

p2 = Path('imsi2/test/temp')
p2.mkdir(parents=True,exist_ok=True) # parents = True : 하위폴더를 여러개 생성 시, 부모-자식 관계를 만들어주는 기능


# ------------------------------------------------
# 4. 파일 생성
# 파일 생성 방법 1
with open('imsi/1.txt','w',encoding='utf-8') as f:
    f.write('홍길동1')
# 파일 생성 방법 2
p = Path('imsi/2.txt')
with open(p,'w',encoding='utf-8') as f2:
    f2.write('홍길동2')
# 파일 생성 방법 3
p3 = Path('imsi/3.txt')
p3.write_text('홍길동3',encoding='utf-8')
# ------------------------------------------------
#  5. 경로 제거

p4 = Path('imsi/3.txt')
p4.unlink()                                     # 바로 삭제, 존재하지않으면 error를 유발하진 않는다.

p5 = Path('imsi')
"""
p5.rmdir() # 안에 파일이나 폴더가 존재하면 삭제 안됨.
"""
# p5.rmdir()

import shutil
shutil.rmtree('imsi2')                          # 삭제하기
