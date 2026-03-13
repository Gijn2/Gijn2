import csv
import requests
from bs4 import BeautifulSoup as bs
import re
from urllib.parse import urljoin
import time
import random

session = requests.Session()

# 고마워요

for i in range(5):
    response = session.get(f"https://www.wepoll.kr/api/v1/polls?page={i+1}&size=10")
    time.sleep(random.uniform(1, 3))
base_url = "https://www.wepoll.kr"
relative_path = "/img/logo.png"


full_url = urljoin(base_url, relative_path)
articles = bs.find_all('div', id=re.compile(r'^article_'))
price_elements = bs.find_all(class_=re.compile(r'price'))

def crawl_multiple_pages(base_url, total_pages):
    all_results = []
    for page_num in range(1, total_pages + 1):
        # URL 파라미터 규칙 적용 (예: ?page=1, ?page=2 ...)
        page_url = f"{base_url}?page={page_num}"
        print(f"현재 {page_num}페이지 수집 중...")
        
        html = get_html(page_url)
        data = parse_data(html)
        
        if not data: # 더 이상 가져올 데이터가 없으면 중단
            break
            
        all_results.extend(data)
        time.sleep(1) # 서버 보호를 위한 지연 (Ethics)
        
    return all_results

def safe_extract(parent_element, selector, attribute=None):
    """
    요소가 없을 경우 에러 대신 None을 반환하는 안전한 추출 함수 (KISS)
    """
    target = parent_element.select_one(selector)
    if not target:
        return None
    
    if attribute:
        return target.get(attribute, "").strip()
    return target.get_text(strip=True)

def get_html(url):
    """
    1. 웹 페이지의 HTML 소스를 가져옵니다. (Network Layer)
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 200 OK가 아니면 예외 발생
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"이미지를 가져오는 중 오류 발생: {e}")
        return None

def parse_data(html):
    """
    2. HTML 내에서 원하는 요소를 추출합니다. (Parsing Layer)
    KISS 원칙에 따라 명확한 CSS Selector를 사용합니다.
    """
    if not html:
        return []

    bs = Beautifulbs(html, 'html.parser')
    results = []

    # [예시] 사이트 구조에 따라 선택자('.item', 'h2', 'a')를 수정하세요.
    # 여기서는 일반적인 뉴스나 상품 리스트 구조를 가정합니다.
    items = bs.select('div.content-item') or bs.find_all('div')[:5] # 예시용 범용 선택자

    for item in items:
        # 제목 추출 (태그가 없을 경우를 대비해 안전하게 처리)
        title_tag = item.find(['h1', 'h2', 'h3', 'a'])
        link_tag = item.find('a')

        if title_tag:
            data = {
                "title": title_tag.get_text(strip=True),
                "link": link_tag.get('href', '#') if link_tag else "No Link"
            }
            results.append(data)
    
    return results

def save_to_csv(data_list, filename="scraped_data.csv"):
    """
    3. 추출된 데이터를 CSV 파일로 저장합니다. (Storage Layer)
    """
    if not data_list:
        print("저장할 데이터가 없습니다.")
        return

    try:
        keys = data_list[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data_list)
        print(f"성공적으로 '{filename}'에 저장되었습니다.")
    except IOError as e:
        print(f"파일 저장 중 오류 발생: {e}")

def main():
    """
    메인 실행 흐름 제어 (Orchestration)
    """
    # 테스트용 URL (실제 크롤링 시 목적지 URL로 변경하세요)
    target_url = "https://www.example.com"
    
    print(f"크롤링 시작: {target_url}...")
    
    # 실행 순서: 요청 -> 파싱 -> 저장
    html_content = get_html(target_url)
    scraped_data = parse_data(html_content)
    save_to_csv(scraped_data)

if __name__ == "__main__":
    main()