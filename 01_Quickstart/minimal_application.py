#!/usr/bin/env python3
# coding:utf-8

from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request



# 初始化一个Flask实例，传参是这个应用或模块的名字
# 这是必需的，以便 Flask 知道在哪里寻找资源，例如模板和静态文件。
app = Flask(__name__)


@app.route("/")
def hello_world():
    # 函数返回在浏览器中显示的消息。默认内容是HTML
    return "<p>Hello, World!</p>"


@app.route("/<name>")  # <name>从url中捕获一个值并传递给视图函数
def hello(name):
    return f"hello, {escape(name)}!"
    # 可能引起注入攻击
    # return f"hello, {name}!"


# 路由变量
# 使用<variable_name>来接收参数
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


# 使用<converter:variable_name>来接收参数,并将其转换为对应类型
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


def do_the_login():
    return "使用POST方式登录成功"

def show_the_login_form():
    return "使用非POST方法，展示表单"

# 测试使用url_for来反向创建url
@app.route('/')
def index():
    return 'index'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))




# 运行程序
# flask --app minimal_application run
# 允许所有地址访问
# flask --app  minimal_application.py run --host=0.0.0.0
