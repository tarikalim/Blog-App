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
        results = db.session.query(Post, Category.name).join(Category).all()
        posts_data = []
        for post, category_name in results:
            post_data = PostDTO(post, category_name)
            posts_data.append(post_data)
        if not posts_data:
            raise PostNotFoundException()
        return posts_data

    @staticmethod
    def get_user_posts(user_id):
        results = db.session.query(Post, Category.name).join(Category).filter(Post.user_id == user_id).all()
        posts_data = []
        for post, category_name in results:
            post_data = PostDTO(post, category_name)
            posts_data.append(post_data)
        if not posts_data:
            raise PostNotFoundException("No posts found for the user")
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
        if not posts_data:
            raise PostNotFoundException(f"No posts found with title '{title}'")
        return posts_data

    @staticmethod
    def get_posts_by_category(category_id):
        results = db.session.query(Post, Category.name).join(Category, Post.category_id == Category.id).filter(
            Post.category_id == category_id).all()
        posts_data = []
        for post, category_name in results:
            post_data = PostDTO(post, category_name)
            posts_data.append(post_data)
        if not posts_data:
            raise PostNotFoundException(f"No posts found for category with ID {category_id}")
        return posts_data

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
        if not post:
            raise PostNotFoundException()

        if title:
            post.title = title
        if content:
            post.content = content

        db.session.commit()
        return post

    @staticmethod
    def delete_post(post_id):
        post = Post.query.get(post_id)
        if not post:
            raise PostNotFoundException()

        db.session.delete(post)
        db.session.commit()
        return None
