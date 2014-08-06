"""
Initialize Flask app

"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

# import cgi
# import webapp2
# from google.appengine.ext.webapp.util import run_wsgi_app

# import MySQLdb
# import os
# import jinja2

app = Flask('apps')
app.config.from_object('apps.settings.Production')

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
 
# import controllers, models
import views, models

