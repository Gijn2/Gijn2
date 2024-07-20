'''
 [과제] 교보문고에서 파이썬 책 검색하여
    - csv 파일로 저장
    - mysql 테이블에 저장
'''


from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv, pymysql

# 교보문고 > '파이썬' 검색 > 국내도서
# html = urlopen("http://www.kyobobook.co.kr/search/SearchKorbookMain.jsp?vPstrCategory=KOR&vPstrKeyWord=python&vPplace=top")
url = 'https://search.kyobobook.co.kr/search?keyword=python&gbCode=TOT&target=total'
html = urlopen(url)
bs = BeautifulSoup(html,'html.parser')

list = bs.select('div.auto_overflow_inner > a.prod_info')

output_file = 'csv/booktitle.csv'
with open(output_file,'w',encoding='utf-8') as w:
    cout = csv.writer(w)
    for i in list:
        print(i.text.replace('\n',''),'작성완료')
        data = i.text.replace('\n', '')
        cout.writerow({data})



conn=pymysql.connect(host='localhost',
                     user='scott',
                     password='tiger',
                     db='basic',
                     charset='utf8')
print('연결성공')

cursor=conn.cursor()
with open('./csv/booktitle.csv','r',encoding='utf-8') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        if not row:
            continue
        for i in range(len(row)):
            data=row[i]
            title=data
            sql="INSERT INTO book(title) VALUES (%s) "
            cursor.execute(sql, (title,))
        conn.commit()
conn.close()
