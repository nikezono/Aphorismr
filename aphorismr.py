# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
 
    Aphorismr

    Flaskrを盛大にパクった箴言集データベース
    nikezono.netのトップページを表示するのに使うのがメインだが
    データベースファイルを分けることによって何にでも使える

"""
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash , Markup , jsonify
import json
import random

# configuration
DATABASE = 'aphorismr.db'
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Creates the database tables."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select text, author, category from entries order by id desc')
    entries = [dict(text=row[0], author=row[1], category=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    g.db.execute('insert into entries (text, author,category) values (?, ?, ?)',
                 [request.form['text'], request.form['author'],request.form['category']])
    g.db.commit()
    flash('New')
    return redirect(url_for('show_entries'))

@app.route('/delete',methods=['POST'])
def delete_entry():
    g.db.execute('delete from entries where text =?',
                   [request.args['text']])
    g.db.commit()
    flash('Deleted')
    return redirect(url_for('show_entries'))

@app.route('/rand')
def random_api():
    cur = g.db.execute('select text, author from entries order by id desc')
    entries = [dict(text=row[0],author=row[1])for row in cur.fetchall()]
    entry = entries[random.randint(0,len(entries)-1)]
    return jsonify(text = entry.pop('text'), author=entry.pop('author'))

if __name__ == '__main__':
    app.run()
