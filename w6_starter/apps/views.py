# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from apps import app, db
from models import Article, Comment
# import MySQLdb
from sqlalchemy import desc


#
# @index & article list
#
@app.route('/', methods=['GET'])
def article_list():
    # data that will be delivered to html file
    context = {}

    # 1. Sort(order) all data in 'article' table (data are created via Article class' instance)
    # 2. Get all data (sorted)
    context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()
    return render_template("home.html", context=context, active_tab='timeline')


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
# Create new article
@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    if request.method == 'GET':  # if the request method is get type
        return render_template('article/create.html', active_tab='article_create')
    elif request.method == 'POST':
        
        article_data = request.form

        # create instance of Aricle class based on User-provided information
        article = Article(
            title=article_data['title'],
            author=article_data['author'],
            category=article_data['category'],
            content=article_data['content']
        )
        
        db.session.add(article)
        db.session.commit()

        flash(u'Article was successfully uploaded.', 'success')
        return redirect(url_for('article_list'))


# Show article in detail
@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    return render_template('article/detail.html')


# Update article
@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    if request.method == 'GET':
        return render_template('article/update.html')
    elif request.method == 'POST':
        return redirect(url_for('article_detail', id=id))


# Delete article
@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'GET':
        return render_template('article/detele.html')
    elif request.method == 'POST':
        return redirect(url_for('article_list'))


#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['POST'])
def comment_create(article_id):
    if request.method == 'GET':
        return render_template('comment/create.html')
    elif request.method == 'POST':
        return redirect(url_for('article_detai', id=article_id))
