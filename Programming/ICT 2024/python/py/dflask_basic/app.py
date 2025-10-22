# app.py

from flask import Flask as fl

app = fl(__name__)

@app.route('/')
def hello_world():

    return "hello world"