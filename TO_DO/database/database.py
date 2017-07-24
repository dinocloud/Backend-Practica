from flask_sqlalchemy import SQLAlchemy
from .. import application


db = SQLAlchemy()
# application.config.from_object(DBSettings)
db.init_app(application)