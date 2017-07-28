from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from settings import *
from flask_cors import CORS


application = Flask(__name__)

db = SQLAlchemy()

def create_app():
    CORS(application)
    application.config.from_object(DBSettings)
    global db
    db = SQLAlchemy()
    db.init_app(application)
    return application