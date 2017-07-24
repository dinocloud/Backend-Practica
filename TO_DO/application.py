from views import *

application = Flask(__name__)


UsersView.register(application)
TasksView.register(application)

if __name__ == '__main__':
    application.run()
