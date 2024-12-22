import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_14")
connection = cx_Oracle.connect(user='admin', password='Ict0397989901', dsn='orcl_high')
print('연결성공')
# 커서 생성
cursor = connection.cursor()

sql = 'SELECT * FROM emp'
cursor.execute(sql)
rows = cursor.fetchall()
print(rows)

# 변경사항 commit
connection.commit()

# 커서, connection 종료
cursor.close()
connection.close()