import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True
    # 通过monkeypatch，动态替换db中的init_db方法，在之后断言时候使用
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    # runner fixture 用于按名称调用 init-db 命令。
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called