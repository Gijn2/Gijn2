'''

    파이썬에서 mysql(mariaDB) 연동 시, 필요한 패키지
        mysql client    : mysql
        pymysql         : 파이썬 sql

'''

import pymysql

conn = pymysql.connect(host='175.114.130.8'
                       ,port=3306
                       ,user='scott'
                       ,password='tiger'
                       ,db='basic'
                       ,charset='utf8')
print('연결성공')

cursor = conn.cursor()
sql = 'select * from emp'
cursor.execute(sql)
rows = cursor.fetchall()

import  csv
output_file = 'files/emp_write.csv'
with open(output_file,'w',encoding='utf-8') as f:
    cout = csv.writer(f)

    for row in rows :
        #print(row)
        cout.writerow(row)
conn.close()