import csv
import requests
from bs4 import BeautifulSoup as bs
import re
from urllib.parse import urljoin
import time
import random
import logging
import os

CONFIG = {
    "TARGET_URL": "https://www.wepoll.kr",
    "TOTAL_PAGES": 5,
    "OUTPUT_FILE": "wepoll_results.csv",
    "TIMEOUT": 10,
    "DELAY_RANGE": (1.0, 2.0)
}


# main() 또는 crawlMultiplePages()에서 사용
scrapedData = [item for item in scrapedData if isValid(item)]

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
    seen_links = set()
    
    for pageNum in range(1, totalPages + 1):
        pageUrl = f"{baseUrl}?page={pageNum}"
        print(f"현재 {pageNum}페이지 수집 중: {pageUrl}")
        
        html = getHtmlWithRetry(pageUrl, session)
        data = parseData(html, baseUrl)

        for item in data:
            if item['link'] not in seen_links:
                allResults.append(item)
                seen_links.add(item['link'])
        
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

def isValid(item):
    # 제목이 2글자 미만이거나 링크가 http로 시작하지 않으면 제외
    if len(item['title']) < 2: return False
    if not item['link'].startswith('http'): return False
    return True


def main():
    # 1. 설정 관리
    target_url = "https://www.wepoll.kr"
    output_file = "wepoll_results.csv"
    
    session = requests.Session()
    
    try:
        # 2. 세션 초기화 (Referer 추가로 보안 우회 확률 높임)
        session.headers.update({
            "Referer": target_url,
            "User-Agent": random.choice(USER_AGENTS)
        })
        
        # 3. 데이터 수집 및 실시간 로그 반영
        logging.info("크롤링 프로세스 시작")
        scrapedData = crawlMultiplePages(target_url, 5, session)
        
        # 4. 데이터 정제 및 유효성 검사 (List Comprehension)
        final_data = []
        for item in scrapedData:
            item['title'] = re.sub(r'\s+', ' ', item['title']).strip()
            if len(item['title']) > 0 and item['link']:
                final_data.append(item)
        
        # 5. 저장 전 결과 확인
        if final_data:
            saveToCsv(final_data, output_file)
            logging.info(f"성공: {len(final_data)}개 저장 완료.")
        else:
            logging.warning("수집된 유효 데이터가 없습니다.")
            
    except KeyboardInterrupt:
        logging.warning("사용자에 의해 중단되었습니다.")
    except Exception as e:
        logging.critical(f"시스템 중단 오류: {e}")
    finally:
        session.close()
        print("작업이 종료되었습니다. 로그 파일(crawling.log)을 확인하세요.")