from views import *
from database import create_app
app = create_app()


UsersView.register(app)
TasksView.register(app)

if __name__ == '__main__':
    app.run()
