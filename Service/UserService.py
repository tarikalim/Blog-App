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
        if username:
            user.username = username
        if email:
            user.email = email
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
