#!/usr/bin/env python3
# coding:utf-8

from flask import Flask

# 初始化一个Flask实例，传参是这个应用或模块的名字
# 这是必需的，以便 Flask 知道在哪里寻找资源，例如模板和静态文件。
app = Flask(__name__)

@app.route("/")
def hello_world():
    # 函数返回在浏览器中显示的消息。默认内容是HTML
    return "<p>Hello, World!</p>"

# 运行程序
# flask --app minimal_application run