from sqlalchemy.exc import SQLAlchemyError

from Model.model import db, Post, Category
from Exception.exception import *


class PostDTO:
    def __init__(self, post, category_name):
        self.id = post.id
        self.user_id = post.user_id
        self.title = post.title
        self.content = post.content
        self.publish_date = post.publish_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        self.category_id = post.category_id
        self.category_name = category_name


class PostService:
    @staticmethod
    def get_all_posts():
        results = db.session.query(Post, Category.name).join(Category).order_by(Post.publish_date.desc()).limit(10).all()
        posts_data = []
        for post, category_name in results:
            post_data = PostDTO(post, category_name)
            posts_data.append(post_data)
        return posts_data

    @staticmethod
    def get_user_posts(user_id):
        results = db.session.query(Post, Category.name).join(Category).filter(Post.user_id == user_id).all()
        posts_data = []
        for post, category_name in results:
            post_data = PostDTO(post, category_name)
            posts_data.append(post_data)
        return posts_data

    @staticmethod
    def get_post_by_id(post_id):
        result = db.session.query(Post, Category.name).join(Category).filter(Post.id == post_id).first()
        if not result:
            raise PostNotFoundException("Post not found")

        post, category_name = result
        return PostDTO(post, category_name)

    @staticmethod
    def get_posts_by_title(title):
        results = db.session.query(Post, Category.name).join(Category, Post.category_id == Category.id).filter(
            Post.title.like(f'%{title}%')).all()
        posts_data = []
        for post, category_name in results:
            post_data = PostDTO(post, category_name)
            posts_data.append(post_data)
        return posts_data

    @staticmethod
    def get_posts_by_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            raise CategoryNotFoundException()
        results = db.session.query(Post, Category.name).join(Category, Post.category_id == Category.id).filter(
            Post.category_id == category_id).all()
        posts_data = []
        for post, category_name in results:
            post_data = PostDTO(post, category_name)
            posts_data.append(post_data)
        return posts_data

    @staticmethod
    def create_post(user_id, title, content, category_id):
        category = Category.query.get(category_id)
        if not category:
            raise CategoryNotFoundException()
        new_post = Post(
            user_id=user_id,
            title=title,
            content=content,
            category_id=category_id
        )
        try:
            db.session.add(new_post)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise PostCreationFailedException()
        return PostDTO(new_post, category.name)

    @staticmethod
    def update_post(post_id, title=None, content=None):
        post = Post.query.get(post_id)
        category = Category.query.get(post.category_id)

        if not post:
            raise PostNotFoundException()

        if title:
            post.title = title
        if content:
            post.content = content

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise PostUpdateFailedException()
        return PostDTO(post, category.name)

    @staticmethod
    def delete_post(post_id):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException()

        try:
            db.session.delete(post)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise PostDeletionFailedException()
        return None
