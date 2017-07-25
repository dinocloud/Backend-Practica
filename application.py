from views import *
from database import create_app
app = create_app()
db.create_all()


UsersView.register(app)
TasksView.register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
