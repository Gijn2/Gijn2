import pymysql

conn = pymysql.connect(host='114.207.167.95'
                       ,port=3306
                       ,user='scott'
                       ,password='tiger'
                       ,db='basic'
                       ,charset='utf8')

print('연결성공')

cursor = conn.cursor()

sql = '''
INSERT INTO emp 
(empno, ename, job, hiredate, sal, comm, deptno)
VALUES (11112,'KANG','IT',now(),1000000000,2000,30)
'''

cursor.execute(sql)
conn.commit()
conn.close()