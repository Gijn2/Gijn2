"""
 - import pathlib 만 선언하면
        Path클래스 사용시 pathlib.Path라고 명시해야 한다. 
"""
from pathlib import Path


# (1) 해당 경로와 하위 목록들 확인
# p = Path('C:\Windows')
"""
p = Path('.')
print(p)
print(p.resolve())  # 리눅스: 디렉토리 
"""

p = Path('C:\Windows')
print(p)
print(p.resolve())
"""
childDirs = []
for x in p.iterdir(): #iterator(요소만 추출) -> Enumeration
    # print(x)
    if x.is_dir():
        childDirs.append(x)
print(childDirs) # 파일 없이 디렉토리들만 list에 담겨서 출력된 모습.
"""

print('-'*100)

# childDirs = [ childDirs.append(x) for x in p.iterdir() if x.is_dir() ]
childDirs = [ x for x in p.iterdir() if x.is_dir() ]
print(childDirs)

p = Path('.')
print(p.resolve())
print('-'*100)
j = list(p.glob('../a_datatype_class/*.py')) # 경로 추출은 항상 중요하다!
print(j)