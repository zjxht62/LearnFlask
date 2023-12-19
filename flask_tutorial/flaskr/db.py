#!/usr/bin/env python3
# coding:utf-8

import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # g 是一个特殊对象，独立于每一个请求。在处理请求过程中，它可以用于储存 可能多个函数都会用到的数据。
        # 所以这里是在每个请求中存储一个数据库的连接
        g.db = sqlite3.connect(
            # current_app该对象指向处理请求的 Flask 应用。这里 使用了应用工厂，那么在其余的代码中就不会出现应用对象。
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row


    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# 定义一个命令行命令
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
# 将数据库相关方法注册到程序
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)