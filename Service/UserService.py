from sqlalchemy.exc import IntegrityError
from Model.model import db, User


class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_users_by_username(username):
        return User.query.filter(User.username.like(f"%{username}%")).all()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def update_user(user_id, username=None, email=None):
        user = User.query.get(user_id)
        try:
            if username and username != user.username:
                if User.query.filter(User.username == username).first():
                    raise ValueError("This username is already taken.")
                user.username = username
            if email and email != user.email:
                if User.query.filter(User.email == email).first():
                    raise ValueError("This email is already used.")
                user.email = email
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Database error, could not update user information.")
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return user
