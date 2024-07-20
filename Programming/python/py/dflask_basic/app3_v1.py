# app3_v1.py
from flask import Blueprint

# app = Blueprint((블루프린트 앱 이름),(보통 __name__ 지정),(url 구분하기 위한 경로))
app = Blueprint('v1', __name__ , url_prefix='/v1')

@app.route('/users')
def users():
    return '여기는 v1/users 입니다.'