from flask import render_template, Flask, request, url_for
from apps import app
import urllib
from bs4 import BeautifulSoup
from google.appengine.ext import db
from flaskext import wtf
from flaskext.wtf import Form, TextField, TextAreaField, \
    SubmitField, validators, ValidationError


# These are decorators!!!! (You learned before)
@app.route('/')  # <homepage address>/
@app.route('/index')  # <homepage address>/index
def index():
    # return "Hello, World! :)"
    return render_template("index.html")


class Photo(db.Model):
    photo = db.BlobProperty()


@app.route('/upload', methods=['GET', 'POST'])
# @app.route('/upload')
def upload():
    if request.files:
        post_data = request.files['photo']
        filestream = post_data.read()
        #filestream = request.files['photo'].read()

        upload_data = Photo()  # declare Photo class type variable
        upload_data.photo = db.Blob(filestream)
        upload_data.put()  # 'put()' function is defined in BlobProperty class.

        # 'url_for' is a function, building url adress where the function havi-
        # ng the name with the first argument
        url = url_for("showssss", key=upload_data.key())

        return render_template("upload.html", url=url)
    else:
        return render_template('upload.html')
"""    form = TwitterForm()

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('upload.html', form=form, url=None)
        else:
            data = DBData()
            data.upload(request.files['photo'], form.message)
            return render_template('upload.html', form=form, url=data.photo_url)

    return render_template('upload.html', form=form, url=None)
"""


@app.route('/upload_db', methods=['POST'])
def upload_db():
    post_data = request.files['photo']
    filestream = post_data.read()
    #filestream = request.files['photo'].read()

    upload_data = Photo()  # declare Photo class type variable
    upload_data.photo = db.Blob(filestream)
    upload_data.put()  # 'put()' function is defined in BlobProperty class.

    # 'url_for' is a function, building url adress where the function having the name with the first argument
    url = url_for("showssss", key=upload_data.key())

    return render_template("upload.html", url=url)


@app.route('/show/<key>', methods=['GET'])
def showssss(key):
    uploaded_data = db.get(key)
    return app.response_class(uploaded_data.photo)
