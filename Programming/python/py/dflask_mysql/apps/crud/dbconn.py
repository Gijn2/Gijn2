# apps / crud / dbconn.py

import pymysql
class Database():
    def __init__(self):
        self.db = pymysql.connect(
            host='localhost',
            user='scott',
            password='tiger',
            db='basic',
            charset='utf8'

        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    # 하나만 가져올것인지(select)
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    # 다 가져올지(select)
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        rows = self.cursor.fetchall()
        return rows

    # insert, delete, update
    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def commit(self):
        self.commit()