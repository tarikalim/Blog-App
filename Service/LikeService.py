from Exception.exception import LikeAlreadyExistsException, PostNotFoundException, LikeNotFoundException
from Model.model import db, Like, Post


class LikeCountDTO:
    def __init__(self, like_count):
        self.like_count = like_count


class LikeDTO:
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


class UserLikeStatusDTO:
    def __init__(self, user_id, post_id, status):
        self.user_id = user_id
        self.post_id = post_id
        self.status = status


class LikeService:

    @staticmethod
    def create_like(user_id, post_id):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException()
        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_like:
            raise LikeAlreadyExistsException()

        new_like = Like(
            user_id=user_id,
            post_id=post_id
        )
        db.session.add(new_like)
        db.session.commit()
        return LikeDTO(new_like.user_id, new_like.post_id)

    @staticmethod
    def delete_like(user_id, post_id):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException()
        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return None
        raise LikeNotFoundException()

    @staticmethod
    def get_post_likes(post_id):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException()
        like_count = Like.query.filter_by(post_id=post_id).count()
        return LikeCountDTO(like_count)

    @staticmethod
    def get_user_like_status(user_id, post_id):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException()
        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if like:
            return UserLikeStatusDTO(like.user_id, like.post_id, True)
        return UserLikeStatusDTO(user_id, post_id, False)
