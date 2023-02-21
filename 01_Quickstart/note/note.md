## Debug Mode
`flask run`命令其实只是启动development server，通过启用debug模式，如果代码更改，服务器将自动重新加载，并且如果在请求期间发生错误，
则会在浏览器中显示交互式调试器。

要启动debug模式，使用`--debug`选项
```shell
$ flask --app hello run --debug
 * Serving Flask app 'hello'
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: nnn-nnn-nnn
```
## HTML转义
当返回HTML的时候（Flask的默认响应类型），为了防止注入攻击，所有用户提交的值，在输出渲染之前，都得被转义。如果使用
Jinja，渲染的HTML模板会自动执行此操作。  
escape() 可以手动转义。因为保持简洁的原 因，在多数示例中它被省略了，但您应该始终留心处理不可信的数据。
```python
from markupsafe import escape

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"
```
## Routing 路由
使用route()注解来将function绑定到URL
```python
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'
```
### 变量规则
+ 使用`<variable_name>`来获取url中的变量
+ 使用`<converter:variable_name>`来获取变量并转换类型
```python
from markupsafe import escape

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
```
![img.png](img.png)
### Unique URLs和重定向行为
下面这两个规则因为末尾是否有斜杠所以使用上有所区别
```python
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```
`projects`的结尾有个斜杠，类似于文件系统中的文件夹的概念，如果访问`/projects`而不加后面的斜杠，Flask会自动重定向到`/projects/

`about`的结尾没有斜杠，类似于文件系统中的一个路径名或者一个文件。如果访问`/about/`多了个斜杠，将会产生一个404 “Not Found“
这有助于使这些资源的 URL 保持唯一，这有助于搜索引擎避免对同一页面进行两次索引。

### URL Building
`url_for`函数用来构建指定函数的URL，第一个参数传的是函数名。之后可以跟任意个关键字参数，每个关键字参数对应URL中的变量。位置变量将添加到
URL中作为查询参数

为啥我们不把URL写死在模板中，而是要使用反转函数`url_for()`来动态构建呢：
1. 反向构建的描述性更好
2. 可以只在一个地方修改URL，不用到处去找
3. URL 创建会为您处理特殊字符的转义，比较直观
4. 生产的路径总是绝对路径，可以避免相对路径产生副作用。
5. 如果您的应用是放在 URL 根路径之外的地方（如在 /myapplication 中，不在 / 中）， url_for() 会为您妥善处理。

### HTTP请求方法
使用同一个URL的时候，应用可以使用多钟HTTP请求方式。默认情况下，route只响应`GET`请求，可以使用route()注解里面的`methods`参数
来处理不同的HTTP请求。
```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
```
上面的示例将路由的所有方法保留在一个函数中，如果每个部分都使用一些公共数据，这将很有用。

还可以将不同方法的视图分成不同的函数。 Flask 为每个常见的 HTTP 方法提供了一种快捷方式，用于使用 get()、post() 等来装饰此类路由。

```python
@app.get('/login')
def login_get():
    return show_the_login_form()

@app.post('/login')
def login_post():
    return do_the_login()
```
如果存在 GET，Flask 会自动添加对 HEAD 方法的支持，并根据 HTTP RFC 处理 HEAD 请求。同样，OPTIONS 会自动为您实现。

## Static Files 静态文件
动态的web应用也需要静态文件，比如通常是CSS和JavaScript文件。理想情况下，你的web服务器提供这些配置，但是在开发过程中，Flask也可以。
只需要在你的包里面或者模块边上创建一个名为`static`的文件夹就行。静态文件位于应用的`/static`中。

使用特定的 'static' 端点就可以生成相应的 URL
```python
url_for('static', filename='style.css')
```
这个静态文件在文件系统中的位置应该是 static/style.css 。

## 渲染模板
在 Python 内部生成 HTML 不好玩，且相当笨拙。因为您必须自己负责 HTML 转义， 以确保应用的安全。因此， Flask 自动为您配置 Jinja2 模板引擎。

使用 render_template() 方法可以渲染模板，您只要提供模板名称和需要作为参数传递给模板的变量就行了。下面是一个简单的模板渲染例子:
```python
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```
Flask 会在 templates 文件夹内寻找模板。因此，如果您的应用是一个模块， 那么模板文件夹应该在模块旁边；如果是一个包，那么就应该在包里面：
1. 一个模块（也就是一个.py）
```python
/application.py
/templates
    /hello.html
```
2. 一个package
```python
/application
    /__init__.py
    /templates
        /hello.html
```
模板示例：
```html
<!doctype html>
<title>Hello from Flask</title>
{% if name %}
  <h1>Hello {{ name }}!</h1>
{% else %}
  <h1>Hello, World!</h1>
{% endif %}
```
在模板内部可以像使用 url_for() 和 get_flashed_messages() 函数一样访问 config 、 request 、 session 和 g 1 对象。

模板在继承使用的情况下尤其有用。其工作原理参见 模板继承 。简单的说，模板继承可以使每个页面 的特定元素（如页头、导航和页尾）保持一致。

自动转义默认开启。因此，如果 name 包含 HTML ，那么会被自动转义。如 果您可以信任某个变量，且知道它是安全的 HTML （例如变量来自一个把 wiki 
标记转换为 HTML 的模块），那么可以使用 Markup 类把 它标记为安全的，或者在模板中使用 |safe 过滤器。更多例子参见 Jinja 2 文档。

下面 Markup 类的基本使用方法:
```shell
from markupsafe import Markup
Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'
Markup('<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>')
Markup.escape('<blink>hacker</blink>')
Markup('&lt;blink&gt;hacker&lt;/blink&gt;')
Markup('<em>Marked up</em> &raquo; HTML').striptags()
'Marked up » HTML'
```
## 操作请求数据
对于 web 应用来说对客户端向服务器发送的数据作出响应很重要。在 Flask 中由全局对象 request 来提供请求信息。如果您有一些 Python 基础，
那么可能会奇怪：既然这个对象是全局的，怎么还能保持线程安全？答案 是本地环境：
### 本地环境
在Flask中的对象确实是全局对象，但是并不是通常意义上的全局对象。这些个对象实际上是特定环境下本地对象的代理。

设想现在处于处理线程的环境中。一个请求进来了，服务器决定生成一个新线程（或者叫其他什么名称的东西，这个下层的东西能够处理包括线程在内的并发系统）。
当Flask 开始其内部请求处理时会把当前线程作为活动环境，并把当前应用和WSGI环境绑定到这个环境（线程）。它以一种聪明的方式使得一个应用可以在不中断的情况下调用另一个应用。

这对您有什么用？基本上您可以完全不必理会。这个只有在做单元测试时才有用。在测试时会遇到由于没有请求对象而导致依赖于请求的代码会突然崩溃的情况。
对策是自己创建一个请求对象并绑定到环境。最简单的单元测试解决方案是使用 test_request_context() 环境管理器。通过使用 with 语句 可以绑定一个测试请求，以便于交互。例如:
```python
from flask import request

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'
```
另一种方式是把整个 WSGI 环境传递给 request_context() 方法:
```python
with app.request_context(environ):
    assert request.method == 'POST'
```
### 请求对象
请求对象在 API 一节中有详细说明这里不细谈（参见 Request ）。 这里简略地谈一下最常见的操作。首先，您必须从 flask 模块导入请求对象:

```python
from flask import request
```
可以使用method属性来获取当前HTTP请求的方法。使用form属性可以获取到使用POST或PUT提交上来的表带数据里面的值
```python
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
```
当 form 属性中不存在这个键时会发生什么？会引发一个 KeyError 。 如果您不像捕捉一个标准错误一样捕捉 KeyError ，那么会显示一个 HTTP 400 Bad Request 错误页面。因此，多数情况下您不必处理这个问题。
要操作 URL （如 ?key=value ）中提交的参数可以使用 args 属性:
```python
searchword = request.args.get('key', '')
```
用户可能会改变 URL 导致出现一个 400 请求出错页面，这样降低了用户友好度。因此，我们推荐使用 get 或通过捕捉 KeyError 来访问 URL 参数。
### 文件上传
在用Flask处理文件上传的时候，需要确保在您的 HTML 表单中设置 enctype="multipart/form-data" 属性就可以了。否则浏览器将不会传送您的文件。
已上传的文件被储存在内存或文件系统的临时位置。您可以通过请求对象 files 属性来访问上传的文件。每个上传的文件都储存在这个 字典型属性中。这个属性基本和标准 Python file 对象一样，另外多出一个 用于把上传文件保存到服务器的文件系统中的 save() 方法。下例展示其如何运作:
```python
from flask import request

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
```
如果想要知道文件上传之前其在客户端系统中的名称，可以使用 filename 属性。但是请牢记这个值是 可以伪造的，永远不要信任这个值。如果想要把客户端的文件名作为服务器上的文件名， 可以通过 Werkzeug 提供的 secure_filename() 函数:
```python
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['the_file']
        file.save(f"/var/www/uploads/{secure_filename(file.filename)}")
    ...
```
### Cookies
要访问 cookies ，可以使用 cookies 属性。可以使用响应 对象 的 set_cookie 方法来设置 cookies 。请求对象的 cookies 属性是一个包含了客户端传输的所有 cookies 的字典。在 Flask 中，如果使用 会话 ，那么就不要直接使用 cookies ，因为 会话 比较安全一些。

读取 cookies:

```python
# 读取cookies
@app.route('/')
def index():
    username = request.cookies.get('username')
    print(f'username in cookie:{username}')
    auth_token = request.cookies.get('auth_token')
    print(f'auth_token in cookie:{auth_token}')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.
    return f"获取到username:{username}\n获取到auth_token:{auth_token}"
```
储存 cookies:
```python
from flask import make_response

@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp
```
注意， cookies 设置在响应对象上。通常只是从视图函数返回字符串， Flask 会把它们转换为响应对象。如果您想显式地转换，那么可以使用 make_response() 函数，然后再修改它。

使用 doc:patterns/deferredcallbacks 方案可以在没有响应对象的情况下设 置一个 cookie 。

## 重定向和错误
使用 redirect() 函数可以重定向。使用 abort() 可以 更早退出请求，并返回错误代码:

```python
from flask import abort, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
```
上例实际上是没有意义的，它让一个用户从索引页重定向到一个无法访问的页面（401 表示禁止访问）。但是上例可以说明重定向和出错跳出是如何工作的。

缺省情况下每种出错代码都会对应显示一个黑白的出错页面。使用 errorhandler() 装饰器可以定制出错页面:

```python
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
```

注意 render_template() 后面的 404 ，这表示页面对就的出错代码是 404 ，即页面不存在。缺省情况下 200 表示：一切正常。

## 关于响应
视图函数的返回值会自动转换为一个响应对象。如果返回值是一个字符串，那么会被 转换为一个包含作为响应体的字符串、
一个 200 OK 出错代码 和一个 text/html 类型的响应对象。如果返回值是一个字典，那么会调用 jsonify() 来产生一个响应。
以下是转换的规则：
1. 如果视图返回的是一个响应对象，那么就直接返回它。
2. 如果返回的是一个字符串，那么根据这个字符串和缺省参数生成一个用于返回的 响应对象。
3. 如果返回的是一个字典，那么调用 jsonify 创建一个响应对象。
4. 如果返回的是一个元组，那么元组中的项目可以提供额外的信息。元组中必须至少 包含一个项目，
且项目应当由 (response, status) 、 (response, headers) 或者 (response, status, headers) 组成。 
status 的值会重载状态代码， headers 是一个由额外头部值组成的列表 或字典。
5. 如果以上都不是，那么 Flask 会假定返回值是一个有效的 WSGI 应用并把它转换为 一个响应对象。

如果想要在视图内部掌控响应对象的结果，那么可以使用 make_response() 函数。

设想有如下视图:

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404
```
可以使用 make_response() 包裹返回表达式，获得响应对象，并对该对象 进行修改，然后再返回:

```python
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

```
### JSON格式的API
一般很多应用都采用JSON格式来响应，如果从视图返回一个`dict`那么它就会被转换为一个JSON响应
```python
@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }
```
如果 dict 还不能满足需求，还需要创建其他类型的 JSON 格式响应，可以使用 jsonify() 函数。该函数会序列化任何支持的 JSON 数据类型。 也可以研究研究 Flask 社区扩展，以支持更复杂的应用。
```python
@app.route("/users")
def users_api():
    users = get_all_users()
    return jsonify([user.to_json() for user in users])
```
## Session 会话
除了请求对象之外还有一种称为 session 的对象，允许您在不同请求 之间储存信息。这个对象相当于用密钥签名加密的 cookie ，即用户可以查看您的 cookie ，但是如果没有密钥就无法修改它。

使用会话之前您必须设置一个密钥。举例说明:

```python
from flask import session

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
```
```
如何生成一个好的密钥
生成随机数的关键在于一个好的随机种子，因此一个好的密钥应当有足够 的随机性。操作系统可以有多种方式基于密码随机生成器来生成随机数据。 使用下面的命令可以快捷的为 Flask.secret_key （ 或者 SECRET_KEY ）生成值:

$ python -c 'import secrets; print(secrets.token_hex())'
'192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
```
基于 cookie 的会话的说明： Flask 会取出会话对象中的值，把值序列化后储 存到 cookie 中。在打开 cookie 的情况下，如果需要查找某个值，但是这个 值在请求中没有持续储存的话，那么不会得到一个清晰的出错信息。请检查页 面响应中的 cookie 的大小是否与网络浏览器所支持的大小一致。

除了缺省的客户端会话之外，还有许多 Flask 扩展支持服务端会话。

## 消息闪现
一个好的应用和用户接口都有良好的反馈，否则到后来用户就会讨厌这个应用。 Flask 通过闪现系统来提供了一个易用的反馈方式。闪现系统的基本工作原理是 在请求结束时记录一个消息，提供且只提供给下一个请求使用。通常通过一个布 局模板来展现闪现的消息。

flash() 用于闪现一个消息。在模板中，使用 get_flashed_messages() 来操作消息。完整的例子参见 消息闪现 。

## 日志
有时候可能会遇到数据出错需要纠正的情况。例如因为用户篡改了数据或客户端 代码出错而导致一个客户端代码向服务器发送了明显错误的 HTTP 请求。多数时 候在类似情况下返回 400 Bad Request 就没事了，但也有不会返回的时候， 而代码还得继续运行下去。

这时候就需要使用日志来记录这些不正常的东西了。自从 Flask 0.3 后就已经为 您配置好 了一个日志工具。

以下是一些日志调用示例:
```python
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')
```
logger 是一个标准的 Logger Logger 类，更多信息详见官方的 logging 文档。

## 集成 WSGI 中间件
如果想要在应用中添加一个 WSGI 中间件，那么可以用应用的 wsgi_app 属性来包装。例如，假设需要在 Nginx 后面使用 ProxyFix 中间件，那么可以这样 做:

```python
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
```
用 app.wsgi_app 来包装，而不用 app 包装，意味着 app 仍旧 指向您的 Flask 应用，而不是指向中间件。这样可以继续直接使用和配置 app 。
## 使用 Flask 扩展
扩展是帮助完成公共任务的包。例如 Flask-SQLAlchemy 为在 Flask 中轻松使用 SQLAlchemy 提供支持。

更多关于 Flask 扩展的内容请参阅 扩展 。

## 部署到网络服务器
已经准备好部署您的新 Flask 应用了？请移步 部署方式 。


