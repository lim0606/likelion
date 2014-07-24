from flask import Flask
import os

app = Flask('apps')
app.config.from_object('apps.config')
import views
