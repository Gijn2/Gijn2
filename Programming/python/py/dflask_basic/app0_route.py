# app.py

from flask import Flask as fl

app = fl(__name__)

@app.route('/')
@app.route('/index')
def hello_world():

    return "hello world2"

@app.route('/users/<username>')
def get_user(username):
    return username+"님이 입장하셨습니다."

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    return str(post_id) + '번 글을 확인'

