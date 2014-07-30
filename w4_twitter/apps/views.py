from flask import render_template, Flask, request, url_for
from apps import app
import urllib
from bs4 import BeautifulSoup
from google.appengine.ext import db
from flaskext import wtf
from flaskext.wtf import Form, TextField, TextAreaField, \
    SubmitField, validators, ValidationError


class Photo(db.Model):
    photo = db.BlobProperty()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
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


@app.route('/show/<key>', methods=['GET'])
def showssss(key):
    uploaded_data = db.get(key)
    return app.response_class(uploaded_data.photo)
