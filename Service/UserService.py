from sqlalchemy.exc import IntegrityError
from Model.model import db, User


class UserDTO:
    def __init__(self, user):
        self.id = user.id
        self.username = user.username
        self.email = user.email
        self.join_date = user.join_date


class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        return UserDTO(user) if user else None

    @staticmethod
    def get_users_by_username(username):
        user = User.query.filter(User.username == username).first()
        return UserDTO(user) if user else None

    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [UserDTO(user) for user in users]

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
            return UserDTO(user)
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Database error, could not update user information.")

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return "User successfully deleted."
        else:
            return "User not found."
