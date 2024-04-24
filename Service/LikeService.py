from Model.model import db, Like, User, Post


class LikeService:

    @staticmethod
    def create_like(user_id, post_id):
        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_like:
            return None  # Post already liked

        new_like = Like(
            user_id=user_id,
            post_id=post_id
        )
        db.session.add(new_like)
        db.session.commit()
        return new_like

    @staticmethod
    def delete_like(user_id, post_id):
        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return True, "Like deleted successfully"
        return False, "Failed to delete like"

    @staticmethod
    def get_post_likes(post_id):
        return Like.query.filter_by(post_id=post_id).count()
