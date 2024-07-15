from flask import flask

app = Flask(__name__)

app.config.from_object("config.DevelopementConfig")

from app import views