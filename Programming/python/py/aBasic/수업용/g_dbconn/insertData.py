import csv,pymysql

fname = './files/emp_write.csv'
try:
    with open(fname,'rt',encoding='utf-8') as f :
        cin = csv.reader(f)
        result = [row for row in cin if row]
        for i in range(len(result)):
            for j in range(1,7):
                print(result[i][j],end=',' if j != 7 else '')
            print(' [{}번 종료]'.format(i))
except Exception as e:
    print('오류발생 :',e)

print('='*100)

conn = pymysql.connect(host='114.207.167.95'
                       ,port=3306
                       ,user='scott'
                       ,password='tiger'
                       ,db='basic'
                       ,charset='utf8')

print('연결성공')

# 커서
cursor = conn.cursor()

sql = '''
    INSERT INTO emp 
    (empno, ename, job, hiredate, sal, comm, deptno)
    VALUES (11112,'KANG','IT',now(),1000000000,2000,30)
'''

