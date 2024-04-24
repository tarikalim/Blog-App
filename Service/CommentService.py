from Model.model import db, Comment, User, Post


class CommentService:

    @staticmethod
    def get_comment_by_id(comment_id):
        return Comment.query.get(comment_id)

    @staticmethod
    def get_all_comments():
        return Comment.query.all()

    @staticmethod
    def create_comment(user_id, post_id, content):
        new_comment = Comment(
            user_id=user_id,
            post_id=post_id,
            content=content
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment

    @staticmethod
    def update_comment(comment_id, user_id, content=None):
        comment = Comment.query.get(comment_id)
        if comment.user_id != user_id:
            return False
        if content:
            comment.content = content
        db.session.commit()
        return comment

    @staticmethod
    def delete_comment(comment_id, user_id):
        comment = Comment.query.get(comment_id)
        if comment and comment.user_id == user_id:
            db.session.delete(comment)
            db.session.commit()
            return True, "Comment deleted successfully"
        return False, "You are not the owner of this comment"

    @staticmethod
    def get_post_comments(post_id):
        return Comment.query.filter_by(post_id=post_id).all()

    @staticmethod
    def get_user_comments(user_id):
        return Comment.query.filter_by(user_id=user_id).all()
