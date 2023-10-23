from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'basketball_db.sqlite3'


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"

    # Creating Database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    from .models import Admin
    from .models import Event
    from .models import Team
    from .models import Match

    # without this login won't be possible
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log-in if you're admin"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    app.register_blueprint(views)
    app.register_blueprint(auth)


    with app.app_context():
        db.create_all()

    return app
