from Model.model import db, Comment, Post
from Exception.exception import *


class CommentDTO:
    def __init__(self, comment):
        self.id = comment.id
        self.user_id = comment.user_id
        self.post_id = comment.post_id
        self.content = comment.content
        self.comment_date = comment.comment_date.strftime(
            '%Y-%m-%dT%H:%M:%SZ')


class CommentService:

    @staticmethod
    def get_comment_by_id(comment_id):
        comment = Comment.query.get(comment_id)
        if not comment:
            raise CommentNotFoundException()
        return CommentDTO(comment)

    @staticmethod
    def create_comment(user_id, post_id, content):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException("Post not found")

        new_comment = Comment(
            user_id=user_id,
            post_id=post_id,
            content=content
        )
        db.session.add(new_comment)
        db.session.commit()

        return CommentDTO(new_comment)

    @staticmethod
    def update_comment(comment_id, content=None):
        comment = Comment.query.get(comment_id)
        if not comment:
            raise CommentNotFoundException()

        if content:
            comment.content = content

        db.session.commit()
        return CommentDTO(comment)

    @staticmethod
    def delete_comment(comment_id):
        comment = Comment.query.get(comment_id)
        if not comment:
            raise CommentNotFoundException()
        db.session.delete(comment)
        db.session.commit()
        return comment

    @staticmethod
    def get_post_comments(post_id):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException("Post not found")

        comments = Comment.query.filter_by(post_id=post_id).all()
        return [CommentDTO(comment) for comment in comments]
