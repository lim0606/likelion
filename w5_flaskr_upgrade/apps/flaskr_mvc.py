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
    entry = {}
    entry['id'] = dataStorage.newid()
    entry['title'] = request.form['title']
    entry['contents'] = request.form['contents']
    entry['datetime'] = datetime.now()
    entry['likecount'] = 0
    dataStorage.put(entry)
    return redirect(url_for('show_entries'))


@app.route('/del/<key>', methods=['GET'])
def del_entry(key):
    dataStorage.delete(key)
    return redirect(url_for('show_entries'))


@app.route('/like/<key>', methods=['GET'])
def like_entry(key):
    entry = dataStorage.select(key)
    entry['likecount'] += 1
    dataStorage.update(key, entry)
    return redirect(url_for('show_entries'))


@app.route('/dislike/<key>', methods=['GET'])
def dislike_entry(key):
    entry = dataStorage.select(key)
    if entry['likecount'] > 0:
        entry['likecount'] -= 1
        dataStorage.update(key, entry)
    return redirect(url_for('show_entries'))


@app.route('/edit/<key>', methods=['GET'])
def edit_entry(key):
    entry = dataStorage.select(key)
    return render_template('edit_entry.html', entry=entry)


@app.route('/apply_edited/<key>', methods=['POST'])
def apply_edited_entry(key):
    entry = dataStorage.select(key)
    entry['id'] = int(key)
    entry['title'] = request.form['title']
    entry['contents'] = request.form['contents']
    entry['datetime'] = datetime.now()
    entry['likecount'] = entry['likecount']
    dataStorage.update(key, entry)
    return redirect(url_for('show_entries'))


from operator import itemgetter


@app.route('/top_entries')
def top_entries():
    entries = dataStorage.out()  # get all entries

    entries = sorted(entries, key=itemgetter('likecount'), reverse=True)
    # the same with the above statement
    # entries = sorted(entries, key=lambda item: item['likecount'], reverse=True)

    # if len(entries) > 3:
    #     return render_template('top_entries.html', entries=entries[1:3])
    # else:
    #     return render_template('top_entries.html', entries=entries)
    return render_template('top_entries.html', entries=entries)
