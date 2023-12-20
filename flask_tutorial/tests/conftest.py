import os
import tempfile

import pytest
from flaskr import  create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        # 覆盖DATABASEkey值，以便使用测试数据库
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

# 测试过程中，将使用client来给应用发送请求，而不需要启动server端
@pytest.fixture
def client(app):
    return app.test_client()

# runner类似于client，它创建一个runner，可以调用在应用程序中注册的Click命令
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Pytest 通过将 fixture 的函数名称与测试函数中的参数名称进行匹配来使用 fixture。


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)