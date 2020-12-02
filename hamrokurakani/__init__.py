from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from .config import Configuration

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(Configuration)
    """ Initiate flask extentions."""
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    """Importing Blueprint packages."""
    from hamrokurakani.admin.routes import admin
    from hamrokurakani.chat.routes import chyat
    from hamrokurakani.users.routes import users
    from hamrokurakani.core.filters import core


    """ Register blueprint app for ready to use."""
    app.register_blueprint(users)
    app.register_blueprint(chyat)
    app.register_blueprint(core)


    admin.init_app(app)
    return app
