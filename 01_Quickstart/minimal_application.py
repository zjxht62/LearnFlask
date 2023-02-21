#!/usr/bin/env python3
# coding:utf-8

from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import request
from flask import render_template
from flask import make_response


# 初始化一个Flask实例，传参是这个应用或模块的名字
# 这是必需的，以便 Flask 知道在哪里寻找资源，例如模板和静态文件。
app = Flask(__name__)


#
# @app.route("/")
# def hello_world():
#     # 函数返回在浏览器中显示的消息。默认内容是HTML
#     return "<p>Hello, World!</p>"


# @app.route("/<name>")  # <name>从url中捕获一个值并传递给视图函数
# def hello(name):
#     return f"hello, {escape(name)}!"
#     # 可能引起注入攻击
#     # return f"hello, {name}!"


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
# @app.route('/')
# def index():
#     return 'index'
#
#
# @app.route('/login')
# def login():
#     return 'login'
#
# @app.route('/user/<username>')
# def profile(username):
#     return f'{username}\'s profile'
#
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))


# 不同的HTTP请求方法，POST和GET
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()


# 渲染模板
# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)

# 处理请求对象
def valid_login(username, password):
    print(username)
    print(password)
    return True


def log_the_user_in(username):
    return f'login success {username}'


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


# 读取cookies
# @app.route('/')
# def index():
#     username = request.cookies.get('username')
#     print(f'username in cookie:{username}')
#     auth_token = request.cookies.get('auth_token')
#     print(f'auth_token in cookie:{auth_token}')
#     # use cookies.get(key) instead of cookies[key] to not get a
#     # KeyError if the cookie is missing.
#     return f"获取到username:{username}\n获取到auth_token:{auth_token}"

@app.route('/')
def index():
    resp = make_response(render_template('hello.html'))
    resp.set_cookie('username', 'the username')
    return resp


# 返回JSON示例
class User:
    def __init__(self):
        self.username = '高启强'
        self.theme = '卖鱼'
        self.image = 'gqq.jpg'

def get_current_user():
    return User()

@app.route("/image/<filename>")
def user_image():
    return "我是图片"

@app.route("/me")
def me_api():
    user = get_current_user()
    app.logger.debug("a debug message")
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }
# 运行程序
# flask --app minimal_application run
# 允许所有地址访问
# flask --app  minimal_application.py run --host=0.0.0.0
