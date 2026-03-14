import csv
import requests
from bs4 import BeautifulSoup as bs
import re
from urllib.parse import urljoin
import time
import random

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def getHtml(url, session):
    headers = {"User-Agent": USER_AGENT}
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"네트워크 오류 발생: {e}")
        return None

# 실패 시 지수 백오프 전략으로 재시도하는 함수
def getHtmlWithRetry(url, session, maxRetries=3):
    for i in range(maxRetries):
        html = getHtml(url, session)
        if html:
            return html
        wait = 2 ** i
        print(f"재시도 중... ({i+1}/{maxRetries}) - {wait}초 대기")
        time.sleep(wait)
    return None

# HTML에서 데이터를 추출하고 상대 경로를 절대 경로로 변환 
def parseData(html, baseUrl):
    if not html:
        return []

    soup = bs(html, 'html.parser')
    results = []

    items = soup.select('div.content-item') or soup.find_all('div', id=re.compile(r'^article_'))[:10]

    for item in items:
        titleTag = item.find(['h1', 'h2', 'h3', 'a'])
        linkTag = item.find('a')

        if titleTag:
            relativeLink = linkTag.get('href', '#') if linkTag else "#"
            fullLink = urljoin(baseUrl, relativeLink)

            results.append({
                "title": titleTag.get_text(strip=True),
                "link": fullLink
            })
    
    return results

# 페이지를 순회하며 데이터 수집 (Orchestration)
def crawlMultiplePages(baseUrl, totalPages, session):

    allResults = []
    for pageNum in range(1, totalPages + 1):
        pageUrl = f"{baseUrl}?page={pageNum}"
        print(f"현재 {pageNum}페이지 수집 중: {pageUrl}")
        
        html = getHtmlWithRetry(pageUrl, session)
        data = parseData(html, baseUrl)
        
        if not data:
            print("더 이상 가져올 데이터가 없습니다.")
            break
            
        allResults.extend(data)
        # Ethics: 서버 부하 방지를 위한 랜덤 지연
        time.sleep(random.uniform(1.0, 2.0))
        
    return allResults

# 데이터를 UTF-8-SIG 인코딩으로 CSV 저장
def saveToCsv(dataList, filename="scraped_data.csv"):
    if not dataList:
        print("저장할 데이터가 없습니다.")
        return

    try:
        keys = dataList[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(dataList)
        print(f"성공적으로 '{filename}'에 저장되었습니다.")
    except IOError as e:
        print(f"파일 저장 중 오류 발생: {e}")

def main():
    targetUrl = "https://www.wepoll.kr"
    totalPages = 1
    session = requests.Session()
    
    print(f"크롤링 시작: {targetUrl}...")
    
    try:
        scrapedData = crawlMultiplePages(targetUrl, totalPages, session)
        saveToCsv(scrapedData, "wepoll_results.csv")
    finally:
        session.close() # 세션 종료
        print("우리")

if __name__ == "__main__":
    main()