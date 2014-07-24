from flask import render_template, Flask, request
from apps import app
import urllib
from bs4 import BeautifulSoup


# These are decorators!!!! (You learned before)
@app.route('/')  # <homepage address>/
@app.route('/index')  # <homepage address>/index
def index():
    # return "Hello, World! :)"
    test = []
    for i in range(0, 10):
        test.append(i)
    return render_template("index.html", a1=test)


@app.route('/profile')
def profile():  # function name has to be different from all others.
    return "<p>My name Jae Hyun Lim </p>"


@app.route('/animal')
def animal():
    age = 21
    species = "Lion"
    friends = ["google", "teacher", "student"]
    return render_template("animal.html",
                           age=age, species=species, friends=friends)


@app.route('/form', methods=['GET', 'POST'])
def form():
    get = None
    post = None

    if request.args:  # if request.args exists
        get = request.args['text_get']

    if request.form:  # if request.form exists
        post = request.form['text_post']

    return render_template("form.html", variable_get=get, variable_post=post)


@app.route('/query', methods=['GET', 'POST'])
def query():
    query_get = None
    query_post = None

    results_get = None
    results_post = None

    if request.args:
        query_get = request.args['query_get']
        results_get = "https://www.google.com/" + \
            "?q=" + query_get + "&gws_rd=ssl&#q=" + query_get

        """htmltext = urllib.urlopen(
            "https://www.google.com/" + "?q=" + query_get + "&gws_rd=ssl&#q=" + query_get).read()

        soup = BeautifulSoup(htmltext, from_encoding="utf-8")
        # print soup

        results_get = []
        for tag in soup.select("h3.r"):
            results_get.append(tag.get_text().encode("utf-8"))
            #print tag

        for result in results_get:
           print result
        """

    if request.form:
        query_post = request.form['query_post']
        results_post = "https://www.google.com/" + \
            "?q=" + query_get + "&gws_rd=ssl&#q=" + query_get

    return render_template("query.html",
                           query_get=query_get,
                           results_get=results_get,
                           query_post=query_post,
                           results_post=results_post)


@app.route('/crawl', methods=['GET', 'POST'])
def crawl():
    #gall = "kangsora"
    query_id = None
    query_page = None

    results = None

    if request.form:
        query_id = request.form['query_id']
        query_page = request.form['query_page']

        address = "http://gall.dcinside.com/board/lists/?id=" + \
            query_id + "&page=" + query_page

        print address

        htmltext = urllib.urlopen("http://www.reddit.com/").read()
        #htmltext = urllib.urlopen(address).read()

        soup = BeautifulSoup(htmltext, from_encoding="utf-8")

        #print soup

        results = []
        for tag in soup.select(".title .may-blank"):
            results.append(tag.get_text())
            #print [tag]

    return render_template("crawl.html",
                           query_id=query_id,
                           query_page=query_page,
                           results=results)
