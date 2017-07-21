from flask import Flask
from Database import db_session
from Views import *

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

app = Flask(__name__)

UsersView.register(app)
TasksView.register(app)

if __name__ == '__main__':
    app.run()