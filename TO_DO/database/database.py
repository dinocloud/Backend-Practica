from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

db = SQLAlchemy()

def create_app():
    # application.config.from_object(DBSettings)
    global db
    db = SQLAlchemy()
    db.init_app(application)
    return application