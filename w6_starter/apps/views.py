# -*- coding: utf-8 -*-
from flask import render_template, request
from apps import app

#
# @index & article list
#
@app.route('/', methods=['GET'])
def article_list():
    # data that will be delivered to html file
    context = {}
    return render_template("home.html", context=context)

#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


#
# article controllers
#
@app.route('/article/create/', methods=['GET','POST'])
