from views import *
from database import create_app, db
from flask_cors import CORS


app = create_app()

prefix = '/api/v1'
UsersView.register(app, route_prefix=prefix)
TasksView.register(app, route_prefix=prefix)


@app.teardown_appcontext
def shutdown_session(response_or_exc):
    try:
        if response_or_exc is None:
            db.session.commit()
    finally:
        db.session.remove()
    return response_or_exc


if __name__ == '__main__':
    with app.app_context():
        CORS(app)
        db.create_all()
        app.run(host='0.0.0.0', debug=True)
