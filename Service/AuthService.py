from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from werkzeug.security import generate_password_hash, check_password_hash
from Helper.sendMail import send_email
from Model.model import db, User
from flask_jwt_extended import create_access_token
from Helper.userValidation import validate_password, validate_email
from flask import current_app


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

    @staticmethod
    def reset_password_request(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return "Error: User not found."

        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps(email, salt='email-confirm')
        reset_link = f"http://localhost:5000/reset-password/{token}"

        try:
            send_email(email, "Password Reset", f"Click the link to reset your password: {reset_link}")
            return "Success: An email has been sent to your email address to reset your password."
        except Exception as e:
            return f"Error: An error occurred while sending the email: {str(e)}"

    @staticmethod
    def change_password(token, new_password):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(token, salt='email-confirm', max_age=1800)  # 30 dakika
        except SignatureExpired:
            return "Error: The link has expired."
        except BadTimeSignature:
            return "Error: Invalid link."

        if not validate_password(new_password):
            return "Error: Password must be at least 8 characters long and contain at least one uppercase letter and one number."

        user = User.query.filter_by(email=email).first()
        if not user:
            return "Error: User not found."
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return "Success: Password has been changed."
