# apps / crud / views.py

from flask import Blueprint, render_template

crud = Blueprint('crud',
                 __name__,
                 static_folder='static',
                 template_folder='templates')

@crud.route('/')
def index():
    return render_template('crud/index.html')


from apps.crud import  dbconn
@crud.route('/dbtest')
def dbtest():
    db_class = dbconn.Database()
    query = "SELECT empno, ename FROM emp"
    rows = db_class.executeAll(query)
    print(rows)
    return render_template('crud/dbtest.html',resultData=rows)