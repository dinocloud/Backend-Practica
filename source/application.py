from views import *
from database import create_app, db
from flask_cors import CORS


app = create_app()

UsersView.register(app)
TasksView.register(app)

if __name__ == '__main__':
    with app.app_context():
        CORS(app)
        db.create_all()
        app.run(host='0.0.0.0', debug=True)
