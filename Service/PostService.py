from model.model import db, Post, User, Category


class PostService:
    @staticmethod
    def get_post_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def get_all_posts():
        return Post.query.all()

    @staticmethod
    def create_post(user_id, title, content, category_id):
        new_post = Post(
            user_id=user_id,
            title=title,
            content=content,
            category_id=category_id
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def update_post(post_id, title=None, content=None):
        post = Post.query.get(post_id)
        if title:
            post.title = title
        if content:
            post.content = content
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post_id):
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return post

    @staticmethod
    def get_user_posts(user_id):
        return Post.query.filter_by(user_id=user_id).all()
