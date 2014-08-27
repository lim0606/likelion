from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

app = Flask('application')
app.config.from_object('application.settings.Production')


db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# # set the secret key.  keep this really ecret:
# import os
# # os.urandom(24)
# # app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# app.secret_key = os.urandom(24)
from secret_keys import SESSION_KEY
app.secret_key = SESSION_KEY

import urls
