"""
    파이썬은 파일하나를 모듈로 취급한다면 다른 파일의 함수를 복사하지 않고 바로 호출한다.

    [주의] import Ex07_alldown1 코드부터 에러발생하지만 실행은 됨

"""


from bs4 import BeautifulSoup
from urllib.parse import *
from urllib.request import *
import os, time, re

# 에러 발생해도 실행은됨_ 폴더 내의 파일을 가져오겠다는 뜻.
import Ex07_alldown1
import Ex07_alldown2

# ------------------------------------------------------
# (3) 이미 처리한 파일인지 확인하기 위한 변수
proc_files = {}

# HTML을 분석하고 다운받는 함수
def analyze_html(url, root_url):
    # (1)
    print("analyze_html=", url)
    savepath = Ex07_alldown2.download_file(url)
    if savepath is None: return       # 없으면 돌아가
    if savepath in proc_files: return # 이미 처리된 파일이면 실행하지 않음, 돌아가
    proc_files[savepath] = True       # 링크가 겹치지 않으면, 해당 링크가 key가 되면서 True라는 value가 추가되는 방법.
    # print(proc_files)

    # (2) 링크 추출
    f = open(savepath, "r", encoding="utf-8")
    html = f.read()
    links = Ex07_alldown1.enum_links(html, url)
        # 읽은 내용을 함수로 보내버리기 -> 읽어서 a태그만 추출하는 방법
    for link_url in links:
        # 링크가 루트 이외의 경로를 나타낸다면 무시 ( 여기서는 docs.python.org 경로가 아니면 무시 )
        if link_url.find(root_url) != 0:
            continue

        # HTML이라면
        # .html로 끝나면,
        if re.search(".html$", link_url):
            # 재귀적으로 HTML 파일 분석하기
            analyze_html(link_url, root_url)
            continue

        # 기타 파일
        Ex07_alldown2.download_file(link_url)
        # 모든 조건을 지나면 또 a tag를 다운받는다
        # 오래 걸려서 도중에 종료를 하면 지금까지 생성된 파일들이 보인다


if __name__ == "__main__":
    # URL에 있는 모든 것 다운받기
    url = "https://docs.python.org/3.5/library/"
    analyze_html(url, url)

# 다운받은 애의 a 태그를 찾아 계속 다운받는 구조. 중복하지 않는 a태그가 있다면 계속 반복함.



