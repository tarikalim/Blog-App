from Model.model import db, Like, User, Post


class LikeService:

    @staticmethod
    def create_like(user_id, post_id):
        new_like = Like(
            user_id=user_id,
            post_id=post_id
        )
        db.session.add(new_like)
        db.session.commit()
        return new_like

    @staticmethod
    def delete_like(like_id, user_id):
        like = Like.query.get(like_id)
        if like and like.user_id == user_id:
            db.session.delete(like)
            db.session.commit()
            return True, "Like deleted successfully"
        return False, "You are not the owner of this like"

    @staticmethod
    def get_post_likes(post_id):
        return Like.query.filter_by(post_id=post_id).count()

    @staticmethod
    def get_user_likes(user_id):
        return Like.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_all_likes():
        return Like.query.all()
