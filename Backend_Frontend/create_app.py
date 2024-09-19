from extensions import db, mail, jwt, migrate, api
from config import Config
from flask import Flask
from API.AuthAPI import auth_ns
from API.UserAPI import user_ns
from API.PostAPI import post_ns
from API.CommentAPI import comment_ns
from API.LikeAPI import like_ns
from API.CategoryAPI import category_ns
from API.FavoriteAPI import favorite_ns
from Exception.error_handler import error_handler


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(user_ns, path='/user')
    api.add_namespace(post_ns, path='/post')
    api.add_namespace(comment_ns, path='/comment')
    api.add_namespace(like_ns, path='/like')
    api.add_namespace(category_ns, path='/category')
    api.add_namespace(favorite_ns, path='/favorite')

    mail.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    error_handler(api)
    api.init_app(app)

    return app
