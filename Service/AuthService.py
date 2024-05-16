from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from Helper.sendMail import send_email
from Model.model import db, User
from flask_jwt_extended import create_access_token
from Helper.userValidation import validate_password, validate_email, validate_username
from flask import current_app
from Exception.exception import (
    UserAlreadyExistsException,
    InvalidPasswordException,
    InvalidEmailException,
    DatabaseOperationException,
    InvalidCredentialsException,
    UserNotFoundException,
    MailSendException,
    TokenExpiredException,
    TokenInvalidException,
    InvalidUsernameException

)


class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter((User.username == username) | (User.email == email)).first():
            raise UserAlreadyExistsException()
        if not validate_username(username):
            raise InvalidUsernameException()
        if not validate_password(password):
            raise InvalidPasswordException()
        if not validate_email(email):
            raise InvalidEmailException()

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseOperationException()
        return new_user

    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return access_token

        raise InvalidCredentialsException()

    @staticmethod
    def reset_password_request(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise UserNotFoundException()

        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps(email, salt='email-confirm')
        reset_link = f"{current_app.config['BASE_URL']}/static/resetpassword.html?token={token}"
        try:
            send_email(email, "Password Reset", f"Click the link to reset your password: {reset_link}")
            return "An email has been sent to your email address to reset your password. Please reset your password within 5 minutes."
        except Exception:
            raise MailSendException()

    @staticmethod
    def change_password(token, new_password):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(token, salt='email-confirm', max_age=300)
        except SignatureExpired:
            raise TokenExpiredException()
        except BadTimeSignature:
            raise TokenInvalidException()

        if not validate_password(new_password):
            raise InvalidPasswordException()
        user = User.query.filter_by(email=email).first()
        if not user:
            raise UserNotFoundException()
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return "Success: Password has been changed."
