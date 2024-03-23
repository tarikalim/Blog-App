from werkzeug.security import generate_password_hash, check_password_hash
from model.model import db, User
from flask_jwt_extended import create_access_token


class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return None

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            return access_token

        return None
