"""
    파일을 다운받고 저장하는 함수

     [참고] 파이썬 정규식 표현 : https://wikidocs.net/4308
"""
from bs4 import BeautifulSoup
from urllib import parse
from urllib import request
import os, time, re  # re : 정규식

def download_file(url):
    p = parse.urlparse(url)
    print('1>',p)
    savepath = './'+p.netloc + p.path
    print('2>',savepath)

    if re.search('/$',savepath): # /로 끝나면
        savepath += 'index.html'
    print('3>',savepath)
    print('='*100)

    if os.path.exists(savepath):
        return savepath

    savedir = os.path.dirname(savepath)
    if not os.path.exists(savedir):
        # os.mkdir()
        os.makedirs(savedir,exist_ok=True) # 존재하지 않으면 디렉토리 생성, 있으면 무시
                                           # 3> 에 해당하는 경로의 모든 디렉토리가 생성됨./ index.html은 생성 안댐
    try:
        request.urlretrieve(url, savepath)
        time.sleep(2)                       # 파일을 받아올때는 반드시 시간을 딜레이 해줄것, 다운받는데 시간이 걸리기 때문.
        return savepath

    except:
        print('fail download',url)
        return None

if __name__ == '__main__':
    url = 'https://docs.python.org/3.6/library/'
    result = download_file(url)
    print(result)