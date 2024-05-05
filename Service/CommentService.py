from Model.model import db, Comment


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
        return CommentDTO(comment) if comment else None

    @staticmethod
    def get_all_comments():
        comments = Comment.query.all()
        return [CommentDTO(comment) for comment in comments]

    @staticmethod
    def create_comment(user_id, post_id, content):
        new_comment = Comment(
            user_id=user_id,
            post_id=post_id,
            content=content
        )
        db.session.add(new_comment)
        db.session.commit()
        return CommentDTO(new_comment)

    @staticmethod
    def update_comment(comment_id, user_id, content=None):
        comment = Comment.query.get(comment_id)
        if not comment or comment.user_id != user_id:
            return False
        if content:
            comment.content = content
        db.session.commit()
        return CommentDTO(comment)

    @staticmethod
    def delete_comment(comment_id, user_id):
        comment = Comment.query.get(comment_id)
        if not comment or comment.user_id != user_id:
            return False, "You are not the owner of this comment"
        db.session.delete(comment)
        db.session.commit()
        return True, "Comment deleted successfully"

    @staticmethod
    def get_post_comments(post_id):
        comments = Comment.query.filter_by(post_id=post_id).all()
        return [CommentDTO(comment) for comment in comments]

    @staticmethod
    def get_user_comments(user_id):
        comments = Comment.query.filter_by(user_id=user_id).all()
        return [CommentDTO(comment) for comment in comments]
