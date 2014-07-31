# -*- coding: utf-8 -*-
# all the imports

from flask import request, redirect, url_for,\
    render_template
from apps import app
from database import Database

from datetime import datetime

dataStorage = Database()


@app.route('/', methods=['GET', 'POST'])
def show_entries():
    entries = dataStorage.out()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    storage = {}
    storage['id'] = dataStorage.newid()
    storage['title'] = request.form['title']
    storage['contents'] = request.form['contents']
    storage['datetime'] = datetime.now()
    storage['likecount'] = 0
    dataStorage.put(storage)
    return redirect(url_for('show_entries'))


@app.route('/del/<key>', methods=['GET'])
def del_entry(key):
    dataStorage.delete(key)
    return redirect(url_for('show_entries'))


@app.route('/like/<key>', methods=['GET'])
def like_entry(key):
    storage = dataStorage.select(key)
    storage['likecount'] += 1
    dataStorage.update(key, storage)
    return redirect(url_for('show_entries'))
