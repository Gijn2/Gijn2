# app3_v2.py

from flask import Blueprint

# app = Blueprint((블루프린트 앱 이름),(보통 __name__ 지정),(url 구분하기 위한 경로))
app = Blueprint('v2', __name__ ,url_prefix='/v2')

@app.route('/users')
def users():
    return '여기는 v2/users 입니다.'
#