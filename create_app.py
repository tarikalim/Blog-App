from extensions import db, mail, jwt, migrate, api
from config import Config
from flask import Flask
from API.AuthAPI import auth_ns




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api.add_namespace(auth_ns, path='/auth')

    mail.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    return app
