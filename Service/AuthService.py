from werkzeug.security import generate_password_hash, check_password_hash
from Model.model import db, User
from flask_jwt_extended import create_access_token
from Helper.userValidation import validate_password, validate_email, validate_mx_record


class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return None
        if not validate_password(password):
            return "Password must be at least 8 characters long and contain at least one uppercase letter and one number."
        if not validate_email(email):
            return "Invalid email format or domain is not valid."

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
            access_token = create_access_token(identity=user.id)
            return access_token

        return None
