# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash, session, g, jsonify
from apps import app, db
from models import (
    Article,
    Comment,
    User
)
from sqlalchemy import desc
from apps.forms import ArticleForm, CommentForm, JoinForm, LoginForm
from werkzeug.security import generate_password_hash, \
    check_password_hash

#
# @index & article list
#


@app.route('/', methods=['GET'])
def article_list():
    # data that will be delivered to html file
    context = {}
    rows = max(Article.query.count() - 5, 5)

    # 1. Sort(order) all data in 'article' table (data are created via Article class' instance)
    # 2. Get all data (sorted)
    context['article_list'] = Article.query.order_by(
        desc(Article.date_created)).limit(rows)
    return render_template("home.html", context=context, active_tab='timeline')


@app.route('/rows')
def article_rows():
    rows = Article.query.count()
    return jsonify(rows=rows)


@app.route('/more')
def article_more():
    last_article_id = request.args.get('last_article_id', 0, type=int)
    
    article_list = Article.query.filter(Article.id < last_article_id).order_by(
        desc(Article.date_created)).limit(5)

    article_result = []
    for article in article_list:
        article_result.append({'id': article.id,
                               'title': article.title,
                               'content': article.content,
                               'author': article.author,
                               'category': article.category,
                               'date_created': article.date_created,
                               })
    # return jsonify(article_list=article_result, count=len(article_result))
    return jsonify(article_list=article_result, count=last_article_id)


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
# @Join controllers
#
@app.route('/user/join/', methods=['GET', 'POST'])
def user_join():
    form = JoinForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                name=form.name.data
            )

            db.session.add(user)
            db.session.commit()

            flash(u'You successfully signed up.', 'success')
            return redirect(url_for('article_list'))

    # if GET
    return render_template('user/join.html', form=form, active_tab='user_join')


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            pwd = form.password.data

            user = User.query.get(email)
            if user is None:
                flash(u'The email is not existed.', 'danger')
            elif not check_password_hash(user.password, pwd):
                flash(u'Password is not matched.', 'danger')
            else:
                session.permanent = True
                session['user_email'] = user.email
                session['user_name'] = user.name

                flash(u'Login completed.', 'success')
                return redirect(url_for('article_list'))
    # if GET
    return render_template('user/login.html', form=form, active_tab='log_in')


@app.route('/logout')
def log_out():
    session.clear()
    # if GET
    return redirect(url_for('article_list'))


@app.before_request
def before_request():
    g.user_name = None

    if 'user_email' in session:
        g.user_email = session['user_email']
        g.user_name = session['user_name']


#
# article controllers
#
# Create new article
@app.route('/article/create/', methods=['GET', 'POST'])
def article_create():
    if g.user_name == None:
        flash(u'Please login.', 'danger')
        return redirect(url_for('log_in'))
    else:
        form = ArticleForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                # create instance of Article class based on User-provided
                # information
                article = Article(
                    title=form.title.data,
                    author=form.author.data,
                    category=form.category.data,
                    content=form.content.data
                )

                db.session.add(article)
                db.session.commit()

                flash(u'Your article was successfully uploaded.', 'success')
                return redirect(url_for('article_list'))

        return render_template('article/create.html', active_tab='article_create', form=form)


# Show article in detail
@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
    article = Article.query.get(id)

    comments = article.comments.order_by(desc(Comment.date_created)).all()

    return render_template('article/detail.html', article=article, comments=comments)


# Update article
@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get(id)
    form = ArticleForm(request.form, obj=article)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(article)
            db.session.commit()
        return redirect(url_for('article_detail', id=id))

    return render_template('article/update.html', form=form)


# Delete article
@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
    if request.method == 'GET':
        return render_template('article/delete.html', article_id=id)
    elif request.method == 'POST':
        article_id = request.form['article_id']
        article = Article.query.get(article_id)
        db.session.delete(article)
        db.session.commit()

        flash('The article was deleted.', 'success')
        return redirect(url_for('article_list'))


#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(
                author=form.author.data,
                mail=form.email.data,
                content=form.content.data,
                password=form.content.data,
                article_id=article_id
            )

            db.session.add(comment)
            db.session.commit()

            flash(u'Your comment was successfully uploaded.', 'success')
        return redirect(url_for('article_detail', id=article_id))
    return render_template('comment/create.html', form=form)


#
# like function
#
@app.route('/article/like/<int:id>', methods=['GET', 'POST'])
def article_like(id):
    article = Article.query.get(id)
    article.like += 1
    db.session.commit()
    return redirect(url_for('article_list'))


#
# dislike function
#
@app.route('/article/dislike/<int:id>', methods=['GET', 'POST'])
def article_dislike(id):
    article = Article.query.get(id)
    if article.like > 0:
        article.like -= 1
    db.session.commit()
    return redirect(url_for('article_list'))
