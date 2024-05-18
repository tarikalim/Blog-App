from sqlalchemy.exc import SQLAlchemyError

from Exception.exception import LikeAlreadyExistsException, PostNotFoundException, LikeNotFoundException, \
    DatabaseOperationException
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


class UserLikedPostDTO:
    def __init__(self, post_id, title):
        self.post_id = post_id
        self.title = title


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
        try:
            db.session.add(new_like)
            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            raise DatabaseOperationException()
        return LikeDTO(new_like.user_id, new_like.post_id)

    @staticmethod
    def delete_like(user_id, post_id):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException()
        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if not like:
            raise LikeNotFoundException()
        try:
            db.session.delete(like)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise DatabaseOperationException()
        return None

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

    @staticmethod
    def get_user_liked_posts(user_id):
        results = db.session.query(Post).join(Like, Post.id == Like.post_id).filter(Like.user_id == user_id).all()
        posts_data = [UserLikedPostDTO(post.id, post.title) for post in results]
        return posts_data
