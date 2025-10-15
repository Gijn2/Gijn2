# apps / app.py

from flask import Flask

def create_app():

    app = Flask(__name__)

    from apps.crud import views as crud_views # import를 중간에 써도되지만 권장하지는 않는다.

    app.register_blueprint(crud_views.crud, url_prefix='/crud')
    # /crud 없이 페이지를 열면 오류 : 페이지를 찾지 못함.
    return app
    # flask run <- 터미널에 입력해서 나오는 주소로 구동