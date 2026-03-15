import csv
import requests
from bs4 import BeautifulSoup as bs
import re
from urllib.parse import urljoin
import time
import random
import logging
import os

logging.basicConfig(
    filename='crawler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crawling.log"),
        logging.StreamHandler()
    ]
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

def getHtml(url, session):

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    
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

# 2026-03-15 수정: 더 유연한 HTML 구조 대응 및 텍스트 정제 추가
# 멋진
def parseData(html, baseUrl):
    if not html: return []
    soup = bs(html, 'html.parser')
    results = []
    
    items = soup.select('div.content-item, div[id^="article_"]')
    
    for item in items:
        titleTag = item.find(['h1', 'h2', 'h3', 'a'])
        if titleTag:
            title = re.sub(r'\s+', ' ', titleTag.get_text(strip=True))
            linkTag = item.find('a', href=True)
            fullLink = urljoin(baseUrl, linkTag['href']) if linkTag else None
            
            if fullLink:
                results.append({"title": title, "link": fullLink})
    
    return results


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
    totalPages = 5
    session = requests.Session()
    # 초기 접속 시 쿠키를 세션에 저장하기 위해 메인 페이지 방문
    session.get(targetUrl, headers={"User-Agent": random.choice(USER_AGENTS)})
    
    try:
        # 데이터 수집
        scrapedData = crawlMultiplePages(targetUrl, totalPages, session)
        
        # 데이터 정제 (공백 제거 등)
        for item in scrapedData:
            item['title'] = re.sub(r'\s+', ' ', item['title']).strip()
            
        saveToCsv(scrapedData, "wepoll_results.csv")
        logging.info(f"총 {len(scrapedData)}개의 데이터를 성공적으로 수집했습니다.")
        
    except Exception as e:
        logging.critical(f"치명적 오류 발생: {e}")
    finally:
        session.close()
        print("모든 작업이 완료되었습니다.")
    