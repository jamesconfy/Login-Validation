from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import ProdConfig

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask("login_validation")
    app.config.from_object(ProdConfig)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from login_validation import routes
        db.create_all()
        login_manager.login_view = "login"
        login_manager.login_message = "You think say you dey wise abi, lol x"
        login_manager.login_message_category = "info"

    return app